import logging
import zmq
from digitalpy.core.zmanager.configuration.zmanager_constants import ZMANAGER_MESSAGE_DELIMITER
from digitalpy.core.zmanager.pusher import Pusher
from digitalpy.core.zmanager.request import Request
from digitalpy.core.parsing.formatter import Formatter

class ZMQPusher(Pusher):
    
    def __init__(self, formatter: Formatter):
        # list of connection to which the socket should reconnect after
        # being unpickled
        self.__pusher_socket_connections = []
        self.pusher_context: zmq.Context = None # type: ignore
        self.pusher_socket: zmq.Socket = None # type: ignore
        self.pusher_formatter: Formatter = formatter
        self.logger = logging.getLogger(self.__class__.__name__)

    def initiate_connections(self, port: int, address: str, service_id: str):
        """initiate subject connection

        Args:
            port (int): subject port
            address (str): subject address
        """
        self.service_id = service_id
        # added to fix hanging connect issue as per 
        # https://stackoverflow.com/questions/44257579/zeromq-hangs-in-a-python-multiprocessing-class-object-solution
        if self.pusher_context == None:
            self.pusher_context = zmq.Context()
        if self.pusher_socket == None:
            self.pusher_socket = self.pusher_context.socket(zmq.PUSH)
        self.pusher_socket.connect(f"tcp://{address}:{port}")
        # add the connection to the connections list so it can be reconnected upon serialization
        self.__pusher_socket_connections.append(f"tcp://{address}:{port}")

    def teardown_connections(self):
        """teardown subject connection
        """
        for connection in self.__pusher_socket_connections:
            self.pusher_socket.disconnect(connection)
        self.pusher_socket.close()
        self.pusher_context.term()
        self.pusher_context.destroy()
        self.pusher_socket = None # type: ignore
        self.pusher_context = None # type: ignore

    def subject_bind(self, address: int, port: str):
        """create the ZMQ zocket

        Args:
            address (int): subject address
            port (str): subject port
        """
        self.pusher_socket.connect(f"tcp://{address}:{port}")
        
    def subject_send_request(self, request: Request, protocol: str, service_id: str = None): # type: ignore
        """send the message to a Puller

        Args:
            request (Request): the request to be sent to the subject
            protocol (str): the protocol of the request to be sent
            service_id (str, optional): the service_id of the request to be sent. Defaults to the id of the current service.
        """
        if service_id is None:
            service_id = self.service_id
            
        # set the service_id so it can be used to create the publish topic by the default routing worker
        request.set_value("service_id", service_id)
        self.pusher_formatter.serialize(request)
        request_msg = ZMANAGER_MESSAGE_DELIMITER.join([request.get_sender().encode(), request.get_context().encode(), request.get_action().encode(), request.get_format().encode(), protocol.encode(), request.get_id().encode(), request.get_values()])
        self.logger.debug("request message: %s", request_msg)
        self.pusher_socket.send(request_msg)
    
    def __getstate__(self):
        state = self.__dict__
        if "pusher_socket" in state:
            del state["pusher_socket"]
        if "pusher_context" in state:
            del state["pusher_context"]
        return state
    
    def __setstate__(self, state):
        self.__dict__ = state
        self.pusher_context = zmq.Context()
        self.pusher_socket = self.pusher_context.socket(zmq.PUSH)
        
        for connection in self.__pusher_socket_connections:
            self.pusher_socket.connect(connection)