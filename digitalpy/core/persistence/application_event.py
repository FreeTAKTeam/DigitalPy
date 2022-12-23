from digitalpy.core.main.event import Event
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.controller import Controller

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