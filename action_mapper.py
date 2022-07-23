from abc import ABC
from request import Request

from response import Response


class ActionMapper(ABC):

    def process_action(self, request: Request, response: Response):
        raise NotImplementedError