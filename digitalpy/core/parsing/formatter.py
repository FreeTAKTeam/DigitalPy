from abc import ABC, abstractmethod
from digitalpy.core.parsing.format import Format
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

class Formatter(ABC):
    
    @abstractmethod
    def get_format(self, name) -> Format:
        """ Get a Format instance from it's name.
        name: The format name
        @return Format
        """
        
    @abstractmethod
    def deserialize(self, request: Request):
        """"""
        
    @abstractmethod
    def serialize(self, response: Response):
        """"""