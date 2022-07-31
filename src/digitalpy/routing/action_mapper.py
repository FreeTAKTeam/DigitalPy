from abc import ABC
from routing.request import Request

from routing.response import Response


class ActionMapper(ABC):

    def process_action(self, request: Request, response: Response):
        raise NotImplementedError