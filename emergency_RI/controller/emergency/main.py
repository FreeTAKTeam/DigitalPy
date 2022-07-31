from urllib import response
from matplotlib.pyplot import get
from regex import E
from routing.controller import Controller
from request import Request
from response import Response

class Emergency(Controller):
    emergencies = {}
    
    def __init__(self):
        pass

    def accept_visitor(self, visitor):
        pass

    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def broadcast_emergencies(self):
        for emergency in self.emergencies:
            self.broadcast_emergency( emergency )
    
    def execute(self, method=None):
        getattr(self, method)()
        return self.response
    
    def receive_emergency(self):
        print('emergencies received')
    
    def broadcast_emergencys(self):
        self.response.set_value("messages", Emergency.emergencies.values())            
        self.response.set_action("Broadcast")
        
    def broadcast_emergency(self, emergency_object):
        pass
