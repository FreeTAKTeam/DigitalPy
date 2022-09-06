from abc import ABC
from digitalpy.routing.request import Request

from digitalpy.routing.response import Response


class ActionMapper(ABC):

    def process_action(self, request: Request, response: Response):
        raise NotImplementedError