from routing.controller import Controller
from routing.request import Request
from routing.response import Response


class TCPCoTClientAcceptor(Controller):
    
    cot_socket = None
    
    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
    
    def execute(self, method=None):
        getattr(self, method)()
        return self.response
    
    def accept_clients(self, clients):
        pass