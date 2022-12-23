import pickle

from digitalpy.core.parsing.abstract_format import AbstractFormat
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

class PickledFormat(AbstractFormat):

    def serialize_values(self, response: Response):
        return pickle.dumps(response.get_values())
        
    def deserialize_values(self, request: Request):
        return pickle.loads(request.get_values())
    