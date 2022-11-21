import pickle

from digitalpy.parsing.impl.abstract_format import AbstractFormat
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response

class PickledFormat(AbstractFormat):

    def serialize_values(self, response: Response):
        return pickle.dumps(response.get_values())
        
    def deserialize_values(self, request: Request):
        return pickle.loads(request.get_values())
    