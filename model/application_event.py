from core.event import Event
from request import Request
from response import Response
from routing.controller import Controller

class ApplicationEvent(Event):
    NAME = "ApplicationEvent"

    BEFORE_ROUTE_ACTION = 'BEFORE_ROUTE_ACTION'

    BEFORE_INITIALIZE_CONTROLLER = 'BEFORE_INITIALIZE_CONTROLLER'

    BEFORE_EXECUTE_CONTROLLER = 'BEFORE_EXECUTE_CONTROLLER'

    AFTER_EXECUTE_CONTROLLER = 'AFTER_EXECUTE_CONTROLLER'

    def __init__(self, stage, request: Request, response: Response = None, controller: Controller = None) -> None:
        self.stage = stage
        self.request = request
        self.response = response
        self.controller = controller

    def get_stage(self):
        return self.stage

    def get_request(self):
        return self.request

    def get_response(self):
        return self.response

    def get_controller(self):
        return self.controller