
from digitalpy.core.zmanager.controller_message import ControllerMessage


class Response(ControllerMessage):

    def set_request(self, request):
        raise NotImplementedError

    def get_request(self):
        raise NotImplementedError

    def set_body(self, body):
        raise NotImplementedError

    def get_body(self):
        raise NotImplementedError