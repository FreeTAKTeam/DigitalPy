import zmq
from typing import List

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

        self.subscriber_context = None
        self.subscriber_socket = None
        self.subscriber_formatter = formatter

    def broker_connect(self, integration_manager_address: str, integration_manager_port: int, integration_manager_protocol: str, service_identity: str, application_protocol: str):
        """Connect or reconnect to broker
        """
        
        if not isinstance(integration_manager_address, str):
            raise TypeError("'integration_manager_address' must be a string")
        if not isinstance(integration_manager_port, int):
            raise TypeError("'integration_manager_port' must be an integer")
        if not isinstance(integration_manager_protocol, str):
            raise TypeError("'integration_manager_protocol' must be a string")
        
        self.service_identity = service_identity

        # added to fix hanging connect issue as per 
        # https://stackoverflow.com/questions/44257579/zeromq-hangs-in-a-python-multiprocessing-class-object-solution
        if self.subscriber_context == None:
            self.subscriber_context = zmq.Context()
        if self.subscriber_socket == None:
            self.subscriber_socket = self.subscriber_context.socket(zmq.SUB)
        self.__subscriber_socket_connections.append(f"{integration_manager_protocol}://{integration_manager_address}:{integration_manager_port}")
        # add the connection to the connections list so it can be reconnected upon serialization
        self.subscriber_socket.connect(f"{integration_manager_protocol}://{integration_manager_address}:{integration_manager_port}")
        self.subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, f"/messages/{service_identity}/")
        self.subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, f"/commands/{service_identity}/")
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.subscriber_socket.setsockopt(zmq.RCVHWM, 0)
        self.subscriber_socket.setsockopt(zmq.SNDHWM, 0)
        
    def broker_receive(self, blocking: bool=False) -> List[Response]:
        """Returns the reply message or None if there was no reply
        Args:
            blocking (False): whether or not the operation is blocking. Option defaults to False.
        """
        responses = []
        try:
            while True:
                if not blocking:
                    message = self.subscriber_socket.recv_multipart(flags=zmq.NOBLOCK)[0].split(b" ", 1)
                else: 
                    message = self.subscriber_socket.recv_multipart()[0].split(b" ", 1)
                # instantiate the response object
                response = ObjectFactory.get_instance("response")
                
                # TODO: this is assuming that the message from the integration manager is pickled
                response.set_format("pickled")

                # get the values returned from the routing proxy and serialize them to
                values = message[1].strip(b",")
                response.set_values(values)
                self.subscriber_formatter.deserialize(response)

                topic = message[0]
                decoded_topic = topic.decode("utf-8")
                topic_sections = decoded_topic.split("/")
                _, _, service_id, protocol, sender, context, action, id, recipients = topic_sections
                response.set_sender(sender)
                response.set_context(context)
                response.set_action(action)
                response.set_id(id)

                if len(recipients.split(RECIPIENT_DELIMITER))>1:
                    response.set_value("recipients", recipients.split(RECIPIENT_DELIMITER)[:-1])

                responses.append(response)

        except zmq.ZMQError as ex:
            return responses

    def broker_send(self, message):
        """Send request to broker
        """
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
            self.subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, f"/messages/{self.service_identity}/")
            self.subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, f"/commands/{self.service_identity}/")