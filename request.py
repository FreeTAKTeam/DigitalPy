from abc import ABC, abstractmethod

from response import Response

from controller_message import ControllerMessage

class Request(ControllerMessage):
    
    def __init__(self, controller=None, context=None, action=None):
        raise NotImplementedError

    @abstractmethod
    def set_response(self, response: Response):
        raise NotImplementedError

    @abstractmethod
    def get_response(self):
        raise NotImplementedError

    @abstractmethod
    def get_method(self):
        raise NotImplementedError

    @abstractmethod
    def set_response_format(self, format):
        raise NotImplementedError

    @abstractmethod
    def get_response_format(self):
        raise NotImplementedError