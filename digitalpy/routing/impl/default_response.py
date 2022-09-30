from digitalpy.routing.impl.abstract_controller_message import AbstractControllerMessage
from digitalpy.routing.response import Response
from digitalpy.routing.request import Request

class DefaultResponse(Response, AbstractControllerMessage):
    def __init__(self):
        super().__init__()
    
    def set_request(self, request: Request):
        self.request = request
        if request.get_response() != self:
            request.set_response(self)
    
    def get_request(self):
        return self.request
    
    def set_status(self, status):
        self.status = status
        
    def get_status(self, status):
        return self.status