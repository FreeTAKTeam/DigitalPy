from digitalpy.core.zmanager.impl.abstract_controller_message import AbstractControllerMessage
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.request import Request

class DefaultResponse(Response, AbstractControllerMessage):
    def __init__(self):
        super().__init__()
    
    def set_request(self, request: Request) -> None:
        """Sets the request object for this response object. If the response object has not been set in the request object, it also sets the response object in the request object.
        Args:
            request (Request): the request object to be set in this response object
        Returns:
            None: returns None"""
        self.request = request
        if request.get_response() != self:
            request.set_response(self)
    
    def get_request(self):
        """
        Gets the request object associated with this response object.

        Returns:
            Request: the request object associated with this response object"""
        return self.request
    
    def set_status(self, status: int) -> None:
        """Sets the status of this response object.
        Args:
            status (int): the status code to be set for this response object
        Returns:
            None: returns None"""
        self.status = status
        
    def get_status(self):
        """Gets the status of this response object.
        Returns:
            int: the status code of this response object"""
        return self.status
