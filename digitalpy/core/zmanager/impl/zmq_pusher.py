import zmq
from digitalpy.core.zmanager.pusher import Pusher
from digitalpy.core.zmanager.request import Request
from digitalpy.core.parsing.formatter import Formatter

class ZMQPusher(Pusher):
    
    def __init__(self, formatter: Formatter):
        self.pusher_context = None
        self.pusher_socket = None
        self.pusher_formatter = formatter

    def initiate_connections(self, port: int, address: str):
        """initiate subject connection

        Args:
            port (int): subject port
            address (str): subject address
        """
        # added to fix hanging connect issue as per 
        # https://stackoverflow.com/questions/44257579/zeromq-hangs-in-a-python-multiprocessing-class-object-solution
        if self.pusher_context == None:
            self.pusher_context = zmq.Context()
        if self.pusher_socket == None:
            self.pusher_socket = self.pusher_context.socket(zmq.PUSH)
        self.pusher_socket.connect(f"tcp://{address}:{port}")

    def subject_bind(self, address: int, port: str):
        """create the ZMQ zocket

        Args:
            address (int): subject address
            port (str): subject port
        """
        self.pusher_socket.connect(f"tcp://{address}:{port}")
        
    def subject_send_request(self, request: Request, protocol: str):
        """send the message to a Puller

        Args:
            request (Request): the request to be sent to the subject
            protocol (str): the protocol of the request to be sent
        """
        self.pusher_formatter.serialize(request)
        self.pusher_socket.send(b",".join([request.get_sender().encode(), request.get_context().encode(), request.get_action().encode(), request.get_format().encode(), protocol.encode(), request.get_values()]))
    
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