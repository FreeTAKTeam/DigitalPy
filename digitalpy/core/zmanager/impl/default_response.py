from digitalpy.core.zmanager.impl.abstract_controller_message import AbstractControllerMessage
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.request import Request

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