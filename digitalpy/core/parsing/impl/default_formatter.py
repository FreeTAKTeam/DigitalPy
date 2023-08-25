from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.parsing.format import Format
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

class DefaultFormatter(Formatter):
    
    def __init__(self, formats: dict):
        self.formats = formats
        
    def get_format(self, name) -> Format:
        if name in self.formats:
            return self.formats[name]
        
    def deserialize(self, request: Request):
        format_name = request.get_format()
        if len(format_name) == 0:
            raise ValueError("no format specified for request %s", request)
        format = self.get_format(format_name)
        format.deserialize(request)
    
    def serialize(self, response: Response):
        format_name = response.get_format()
        if len(format_name) == 0:
            raise ValueError("no format specified for response %s", response)
        format = self.get_format(format_name)
        format.serialize(response)
        