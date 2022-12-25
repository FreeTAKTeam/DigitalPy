import logging
import re
from typing import Dict

from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

class DefaultHealthCheckController(Controller):
    """Controller for performing health checks on a component"""

    def __init__(
        self,
        request: Request,
        response: Response,
        domain_action_mapper: ActionMapper,
        configuration: Configuration,
        **kwargs,
    ):
        super().__init__(request, response, domain_action_mapper, configuration)

    def execute(self, method: str = None):
        """Execute the specified method"""
        try:
            getattr(self, method)(**self.request.get_values())
        except Exception as e:
            logging.exception("Error executing health check")
            self.response.set_value("health", False)
            self.response.set_value("error", str(e))

    def get_health(self, logger: logging.Logger, **kwargs) -> None:
        """Check the component's health by searching for critical errors in the log file

        Args:
            logger: logger for the component

        Returns:
            None: the health and error are set on the response object
        """
        healthy = True
        error = ""

        # read the log file in chunks and search for critical errors
        chunk_size = 4096  # read the log file in 4KB chunks
        with open(logger.parent.handlers[0].baseFilename, "r") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:  # end of file reached
                    break
                if re.search(".* CRITICAL .*", chunk):
                    healthy = False
                    error = chunk
                    break

        self.response.set_value("health", healthy)
        self.response.set_value("error", error)
