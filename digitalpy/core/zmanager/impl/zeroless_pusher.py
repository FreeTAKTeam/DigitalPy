from zeroless import Client
from digitalpy.core.zmanager.pusher import Pusher
from digitalpy.core.zmanager.request import Request
from digitalpy.core.parsing.formatter import Formatter

class ZerolessPusher(Pusher):
    
    def __init__(self, formatter: Formatter):
        
        self.pusher_connected = False
        self.push = None
        self.pusher_formatter = formatter

    def initiate_connections(self, port: int, address: str):
        self.pusher_client = Client()
        if port and address:
            self.subject_bind(address, port)

    def subject_bind(self, address: int, port: str):
        """create the ZMQ zocket
        """
        self.pusher_client.connect(address, port)
        self.push = self.pusher_client.push()
        
    def subject_send_request(self, request: Request):
        """send the message to a Puller
        """
        serialized_request = self.pusher_formatter.serialize(request)
        self.push(serialized_request)