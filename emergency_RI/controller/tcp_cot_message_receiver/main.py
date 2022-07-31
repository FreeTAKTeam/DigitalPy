from routing.controller import Controller
from routing.request import Request
from routing.response import Response


class TCPCoTMessageReceiver(Controller):
    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def execute(self, method=None):
        getattr(self, method)()
        return self.response
    
    def receive_messages(self):
        pass