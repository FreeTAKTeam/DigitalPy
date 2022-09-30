from abc import ABC, abstractmethod
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response

class Format(ABC):
    
    @abstractmethod
    def deserialize(self, request: Request):
        """deserialize the request from the external representation to an internal object"""
    
    @abstractmethod
    def serialize(self, response: Response):
        """serialize response data according to the external representation"""
        
    