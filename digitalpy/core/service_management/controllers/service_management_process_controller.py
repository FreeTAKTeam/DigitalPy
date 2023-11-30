from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response


class ServiceManagementProcessController(Controller):
    """ Service Management Process Controller class. Responsible for handling all operations on
    a service's underlying process.
    """

    def __init__(self, request: Request, response: Response, action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, action_mapper, configuration)
        