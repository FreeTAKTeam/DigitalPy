import zmq
from typing import Optional
import logging
from digitalpy.core.zmanager.controller_message import ControllerMessage
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER,
)
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)

RECIPIENT_DELIMITER = ";"


class IntegrationManagerSubscriber:
    """This class is responsible for managing subscription connections to the integration manager."""

    def __init__(
        self,
        formatter: Formatter,
        timeout: int,
        service_id: Optional[str] = None,
        application_protocol: Optional[str] = None,
    ):
        # list of connection to which the socket should reconnect after
        # being unpickled
        self.__subscriber_socket_connections = []

        self.subscriber_context: zmq.Context = None  # type: ignore
        self.subscriber_socket: zmq.Socket = None  # type: ignore
        self.subscriber_formatter = formatter
        self.logger = logging.getLogger(self.__class__.__name__)

        self.service_id = service_id
        self.application_protocol = application_protocol
        conf: Configuration = ObjectFactory.get_instance("Configuration")

        self.integration_manager_address = conf.get_value(
            "integration_manager_publisher_address", "IntegrationManager"
        )
        self.integration_manager_port = conf.get_value(
            "integration_manager_publisher_port", "IntegrationManager"
        )
        self.integration_manager_protocol = conf.get_value(
            "integration_manager_publisher_protocol", "IntegrationManager"
        )

        self.timeout = timeout

        self.action_key_controller: ActionKeyController = ObjectFactory.get_instance(
            "ActionKeyController"
        )

    def setup(self):
        """Connect or reconnect to integration manager"""

        # added to fix hanging connect issue as per
        # https://stackoverflow.com/questions/44257579/zeromq-hangs-in-a-python-multiprocessing-class-object-solution
        self.subscriber_context = zmq.Context()
        self.subscriber_socket = self.subscriber_context.socket(zmq.SUB)

        self.__subscriber_socket_connections.append(
            f"{self.integration_manager_protocol}://{self.integration_manager_address}:{self.integration_manager_port}"
        )

        # add the connection to the connections list so it can be reconnected upon serialization
        self.subscriber_socket.connect(
            f"{self.integration_manager_protocol}://{self.integration_manager_address}:{self.integration_manager_port}"
        )

        self._subscribe_to_topics()

        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.subscriber_socket.setsockopt(zmq.RCVHWM, 0)
        self.subscriber_socket.setsockopt(zmq.SNDHWM, 0)

        self.set_blocking(True)
        self.set_timeout(self.timeout)

    def _get_topics(self) -> list[ActionKey]:
        topics = []
        return topics

    def _subscribe_to_topics(self):
        for topic in self._get_topics():
            self.subscribe_to_action(topic)

    def subscribe_to_action(self, action_key: ActionKey):
        """Subscribe to a topic

        Args:
            action_key (ActionKey): the action key to subscribe to
        """
        topic = self.action_key_controller.serialize_to_generic_topic(action_key)
        self.subscriber_socket.setsockopt(zmq.SUBSCRIBE, topic)

    def teardown(self):
        """Disconnect from broker"""
        for connection in self.__subscriber_socket_connections:
            self.subscriber_socket.disconnect(connection)
        self.subscriber_socket.close()
        self.subscriber_context.term()
        self.subscriber_context.destroy()

    def fetch_integration_manager_request(self) -> Optional[Request]:
        """receive the next response from the integration manager"""
        try:
            message = self._receive_message()

            return self._deserialize_request(message)
        except zmq.error.Again:
            return None

    def fetch_integration_manager_response(self) -> Optional[Response]:
        try:
            message = self._receive_message()

            return self._deserialize_response(message)
        except zmq.error.Again:
            return None

    def _receive_message(self) -> list[bytes]:
        message = self.subscriber_socket.recv_multipart()[0].split(b" ", 1)

        return message

    def _deserialize_controller_message(self, message: list[bytes], controller_message: ControllerMessage) -> ControllerMessage:
        # TODO: this is assuming that the message from the integration manager is pickled
        controller_message.set_format("pickled")

        # get the values returned from the routing proxy and serialize them to
        values: bytes = message[1].strip(ZMANAGER_MESSAGE_DELIMITER)
        controller_message.set_values(values)
        self.subscriber_formatter.deserialize(controller_message)

        topic = message[0]
        decoded_topic = topic.decode("utf-8")
        topic_sections = decoded_topic.split("/", 9)
        _, _, service_id, protocol, sender, context, action, id, recipients = (
            topic_sections
        )
        controller_message.set_sender(sender)
        controller_message.set_context(context)
        controller_message.set_action(action)
        controller_message.set_id(id)
        return controller_message

    def _deserialize_response(self, message: list[bytes]) -> Response:
        response: Response = ObjectFactory.get_new_instance("Response")
        response = self._deserialize_controller_message(message, response)
        return response
    
    def _deserialize_request(self, message: list[bytes]) -> Request:
        request: Request = ObjectFactory.get_new_instance("Request")
        request = self._deserialize_controller_message(message, request)
        return request

    def set_blocking(self, blocking: bool):
        """Set the blocking mode of the socket"""
        if blocking:
            self.subscriber_socket.setsockopt(zmq.RCVTIMEO, -1)
        else:
            self.subscriber_socket.setsockopt(zmq.RCVTIMEO, self.timeout)

    def set_timeout(self, timeout: int):
        """Set the timeout for the socket"""
        self.timeout = timeout
        self.subscriber_socket.setsockopt(zmq.RCVTIMEO, self.timeout)

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
                zmq.SUBSCRIBE, f"/messages/{self.service_id}/"
            )
            self.subscriber_socket.setsockopt_string(
                zmq.SUBSCRIBE, f"/commands/{self.service_id}/"
            )
