from zeroless import Client
from digitalpy.core.zmanager.pusher import Pusher
from digitalpy.core.zmanager.request import Request
from digitalpy.core.parsing.formatter import Formatter

class ZerolessPusher(Pusher):
    
    def __init__(self, formatter: Formatter):
        self.push = None
        self.pusher_formatter = formatter

    def initiate_connections(self, port: int, address: str):
        """initiate the connections to the subject

        Args:
            port (int): the subject port
            address (str): the subject address
        """
        self.pusher_client = Client()
        if port and address:
            self.subject_bind(address, port)

    def subject_bind(self, address: int, port: str):
        """create the ZMQ zocket
        """
        self.pusher_client.connect(address, port)
        
    def subject_send_request(self, request: Request, protocol: str):
        """send the message to a Puller
        """
        push = self.pusher_client.push()
        self.pusher_formatter.serialize(request)
        push(b",".join([request.get_sender().encode(), request.get_context().encode(), request.get_action().encode(), request.get_format().encode(), protocol.encode(), request.get_values()]))