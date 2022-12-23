from abc import ABC, abstractmethod

from digitalpy.core.zmanager.response import Response

from digitalpy.core.zmanager.controller_message import ControllerMessage

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
