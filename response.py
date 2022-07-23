from request import Request

class Response(ControllerMessage):

    def set_request(self, request: Request):
        raise NotImplementedError

    def get_request(self):
        raise NotImplementedError

    def set_body(self, body):
        raise NotImplementedError

    def get_body(self):
        raise NotImplementedError