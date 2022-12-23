from zeroless import Client
from digitalpy.core.zmanager.pusher import Pusher
from digitalpy.core.zmanager.request import Request
from digitalpy.core.parsing.formatter import Formatter

class ZerolessPusher(Pusher):
    
    def __init__(self, port: int, address: str, formatter: Formatter):
        self.client = Client()
        self.connected = False
        self.push = None
        self.formatter = formatter
        if port and address:
            self.subject_bind(port, address)

    def subject_bind(self, port: int, address: str):
        """create the ZMQ zocket
        """
        self.client.connect(port, address)
        self.push = self.client.push()
        
    def subject_send_request(self, request: Request):
        """send the message to a Puller
        """
        serialized_request = self.formatter.serialize(request)
        self.push(serialized_request)