from digitalpy.core.zmanager.impl.abstract_controller_message import AbstractControllerMessage
from digitalpy.core.zmanager.request import Request
import json

class DefaultRequest(Request, AbstractControllerMessage):

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
    