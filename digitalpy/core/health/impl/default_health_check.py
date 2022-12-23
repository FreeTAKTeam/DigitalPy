from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
import re


class DefaultHealthCheckController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        domain_action_mapper: ActionMapper,
        configuration: Configuration,
        **kwargs,
    ):
        super().__init__(request, response, domain_action_mapper, configuration)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())

    def get_health(self, logger, **kwargs):
        """get whether or not the component is healthy,
        healthy is defined as having no fatal errors."""
        healthy = True
        error = ""
        with open(logger.parent.handlers[0].baseFilename, "r") as f:
            lines = f.readlines()
            lines.reverse()
            for line in lines:
                if re.match(".* CRITICAL .*", line):
                    healthy = False
                    error = line
        self.response.set_value("health", healthy)
        self.response.set_value("error", error)
