from abc import ABC, abstractmethod

from routing.response import Response

from routing.controller_message import ControllerMessage

class Request(ControllerMessage):

    @abstractmethod
    def set_response(self, response: Response):
        raise NotImplementedError

    @abstractmethod
    def get_response(self):
        raise NotImplementedError

    @abstractmethod
    def get_method(self):
        raise NotImplementedError
