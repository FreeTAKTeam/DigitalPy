from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response


class TCPCoTMessageReceiver(Controller):
    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def execute(self, method=None):
        getattr(self, method)()
        return self.response
    
    def receive_messages(self):
        pass