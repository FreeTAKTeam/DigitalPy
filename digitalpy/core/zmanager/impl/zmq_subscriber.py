import time
import zmq
from typing import List, Union, Dict
import logging
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER,
)

from digitalpy.core.zmanager.subscriber import Subscriber
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.formatter import Formatter

RECIPIENT_DELIMITER = ";"


class ZmqSubscriber(Subscriber):
    # 1. Create a context
    # 2. Create a socket
    # 3. Connect to the socket
    # 4. Subscribe to the socket
    # 5. Receive the message
    # 6. Close the socket
    # 7. Destroy the context
    def __init__(self, formatter: Formatter):
        # list of connection to which the socket should reconnect after
        # being unpickled
        self.__subscriber_socket_connections = []

        self.subscriber_context: zmq.Context = None  # type: ignore
        self.subscriber_socket: zmq.Socket = None  # type: ignore
        self.subscriber_formatter = formatter
        self.logger = logging.getLogger(self.__class__.__name__)
        self.responses: Dict[str, Response] = {}

    def broker_connect(
        self,
        integration_manager_address: str,
        service_identity: str,
        application_protocol: str,
    ):
        """Connect or reconnect to broker"""

        if not isinstance(integration_manager_address, str):
            raise TypeError("'integration_manager_address' must be a string")

        self.service_identity = service_identity

        # added to fix hanging connect issue as per
        # https://stackoverflow.com/questions/44257579/zeromq-hangs-in-a-python-multiprocessing-class-object-solution
        if self.subscriber_context == None:
            self.subscriber_context = zmq.Context()
        if self.subscriber_socket == None:
            self.subscriber_socket = self.subscriber_context.socket(zmq.SUB)
        self.__subscriber_socket_connections.append(integration_manager_address)
        # add the connection to the connections list so it can be reconnected upon serialization
        self.subscriber_socket.connect(integration_manager_address)
        self.subscriber_socket.setsockopt_string(
            zmq.SUBSCRIBE, f"/messages/{service_identity}/"
        )
        # currently nothing is done with the commands endpoint but it will be used in future
        self.subscriber_socket.setsockopt_string(
            zmq.SUBSCRIBE, f"/commands/{service_identity}/"
        )
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.subscriber_socket.setsockopt(zmq.RCVHWM, 0)
        self.subscriber_socket.setsockopt(zmq.SNDHWM, 0)

    def broker_disconnect(self):
        """Disconnect from broker"""
        for connection in self.__subscriber_socket_connections:
            self.subscriber_socket.disconnect(connection)
        self.subscriber_socket.close()
        self.subscriber_context.term()
        self.subscriber_context.destroy()

    def broker_receive_response(
        self, request_id: str, blocking: bool = True, timeout=1, retry=0
    ) -> Union[Response, None]:
        """Returns the reply message or None if there was no reply"""
        try:
            s_time = time.time()
            while s_time + timeout > time.time() and retry >= 0:
                if not blocking:
                    message = self.subscriber_socket.recv_multipart(flags=zmq.NOBLOCK)[
                        0
                    ].split(b" ", 1)
                else:
                    self.subscriber_socket.setsockopt(zmq.RCVTIMEO, timeout * 1000)
                    message = self.subscriber_socket.recv_multipart()[0].split(b" ", 1)
                # instantiate the response object
                response: Response = ObjectFactory.get_new_instance("response")

                # TODO: this is assuming that the message from the integration manager is pickled
                response.set_format("pickled")

                # get the values returned from the routing proxy and serialize them to
                values = message[1].strip(ZMANAGER_MESSAGE_DELIMITER)
                response.set_values(values)
                self.subscriber_formatter.deserialize(response)

                topic = message[0]
                decoded_topic = topic.decode("utf-8")
                topic_sections = decoded_topic.split("/")
                _, _, service_id, protocol, sender, context, action, id, recipients = (
                    topic_sections
                )
                response.set_sender(sender)
                response.set_context(context)
                response.set_action(action)
                response.set_id(id)

                if len(recipients.split(RECIPIENT_DELIMITER)) > 1:
                    response.set_value(
                        "recipients", recipients.split(RECIPIENT_DELIMITER)[:-1]
                    )
                if response.get_id() == request_id:
                    return response
                else:
                    self.responses[response.get_id()] = response
                    retry -= 1
            return None
        except zmq.ZMQError as ex:
            return None

    def broker_receive(
        self, blocking: bool = False, max_messages: int = 100
    ) -> List[Response]:
        """Returns the reply message or None if there was no reply
        Args:
            blocking (False): whether or not the operation is blocking. Option defaults to False.
            max_messages (100): the maximum number of messages to receive. Option defaults to 100.
        """
        responses = []
        try:
            for _ in list(self.responses.values()):
                responses.append(list(self.responses.values()).pop(0))
            # TODO: move the range to a configuration file
            # this protects against the case where messages are being sent faster than they can be received
            for _ in range(max_messages):
                if not blocking:
                    message = self.subscriber_socket.recv_multipart(flags=zmq.NOBLOCK)[
                        0
                    ].split(b" ", 1)
                else:
                    message = self.subscriber_socket.recv_multipart()[0].split(b" ", 1)
                # instantiate the response object
                response: Response = ObjectFactory.get_new_instance("response")

                # TODO: this is assuming that the message from the integration manager is pickled
                response.set_format("pickled")

                # get the values returned from the routing proxy and serialize them to
                values = message[1].strip(ZMANAGER_MESSAGE_DELIMITER)
                response.set_values(values)
                self.subscriber_formatter.deserialize(response)

                topic = message[0]
                decoded_topic = topic.decode("utf-8")
                topic_sections = decoded_topic.split("/", 9)
                _, _, service_id, protocol, sender, context, action, id, recipients = (
                    topic_sections
                )
                response.set_sender(sender)
                response.set_context(context)
                response.set_action(action)
                response.set_id(id)

                if len(recipients.split(RECIPIENT_DELIMITER)) > 1:
                    response.set_value(
                        "recipients", recipients.split(RECIPIENT_DELIMITER)[:-1]
                    )
                else:
                    response.set_value("recipients", "*")

                responses.append(response)
            return responses

        except zmq.ZMQError as ex:
            return responses

    def broker_send(self, message):
        """Send request to broker"""
        self.subscriber_socket.send(message)

    def __getstate__(self):
        state = self.__dict__
        if "subscriber_socket" in state:
            del state["subscriber_socket"]
        if "subscriber_context" in state:
            del state["subscriber_context"]
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.subscriber_context = zmq.Context()
        self.subscriber_socket = self.subscriber_context.socket(zmq.SUB)
        for connection in self.__subscriber_socket_connections:
            self.subscriber_socket.connect(connection)
            self.subscriber_socket.setsockopt_string(
                zmq.SUBSCRIBE, f"/messages/{self.service_identity}/"
            )
            self.subscriber_socket.setsockopt_string(
                zmq.SUBSCRIBE, f"/commands/{self.service_identity}/"
            )
