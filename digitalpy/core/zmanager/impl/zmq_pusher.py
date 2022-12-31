import zmq
from digitalpy.core.zmanager.pusher import Pusher
from digitalpy.core.zmanager.request import Request
from digitalpy.core.parsing.formatter import Formatter

class ZMQPusher(Pusher):
    
    def __init__(self, formatter: Formatter):
        self.pusher_context = zmq.Context()
        self.pusher_formatter = formatter
        self.pusher_socket = self.pusher_context.socket(zmq.PUSH)

    def initiate_connections(self, port: int, address: str):
        self.pusher_socket.connect(f"tcp://{address}:{port}")

    def subject_bind(self, address: int, port: str):
        """create the ZMQ zocket
        """
        self.pusher_socket.connect(f"tcp://{address}:{port}")
        
    def subject_send_request(self, request: Request, protocol: str):
        """send the message to a Puller
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