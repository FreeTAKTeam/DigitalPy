import time
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.service_management.domain.service import Service
from digitalpy.core.service_management.digitalpy_service import DigitalPyService


class DemoService(DigitalPyService):
    """Demo service class."""

    def __init__(self, formatter: Formatter, service: Service):
        super().__init__(service_id="demo_service", formatter=formatter, service=service)

    def initialize(self):
        """Initialize the service."""
        pass

    def start(self):
        """Start the service."""
        # simulate work
        time.sleep(5)

    def stop(self):
        """Stop the service."""
        pass

    def restart(self):
        """Restart the service."""
        pass

    def status(self):
        """Get the status of the service."""
        pass