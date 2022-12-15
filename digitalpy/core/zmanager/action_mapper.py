from abc import ABC
from digitalpy.core.zmanager.request import Request

from digitalpy.core.zmanager.response import Response


class ActionMapper(ABC):

    def process_action(self, request: Request, response: Response):
        raise NotImplementedError