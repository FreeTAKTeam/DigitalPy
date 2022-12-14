from zeroless import Client
from digitalpy.routing.pusher import Pusher

class ZerolessPusher(Pusher):
    
    def __init__(self, port: int, address: str):
        self.client = Client()
        self.connected = False
        self.push = None
        if port and address:
            self.subject_bind(port, address)

    def subject_bind(self, port: int, address: str):
        """create the ZMQ zocket
        """
        self.client.connect(port, address)
        self.push = self.client.push()
        
    def subject_send(self, message: str):
        """send the message to a Puller
        """
        self.push(message)