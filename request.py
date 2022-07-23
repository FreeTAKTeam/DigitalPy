from abc import ABC

class Request(ControllerMessage):
    
    def __init__(self, controller=None, context=None, action=None):
        raise NotImplementedError

    def set_response(self, response: Response):
        raise NotImplementedError

    def get_response(self):
        raise NotImplementedError

    def get_method(self):
        raise NotImplementedError

    def set_response_format(self, format):
        raise NotImplementedError

    def get_response_format(self):
        raise NotImplementedError