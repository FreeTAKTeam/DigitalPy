from routing.controller_message import ControllerMessage
from request import Request


class DefaultRequest(Request):

    def __init__(self):
        super().__init__()
        self.response = None
        self.method = None
        
    def set_response(self, response):
        self.response = response
        if response.get_request != self:
            response.set_request(self)
    
    def get_response(self):
        return self.response

    def get_method(self):
        return self.method
    