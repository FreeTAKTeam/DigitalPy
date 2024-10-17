import time
from digitalpy.core.zmanager.impl.integration_manager_subscriber import IntegrationManagerSubscriber
from digitalpy.core.zmanager.impl.subject_pusher import SubjectPusher
from digitalpy.core.service_management.domain.model.service_configuration import ServiceConfiguration
from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from unittest.mock import MagicMock
from multiprocessing import Process

class DemoService(DigitalPyService):
    """Demo service class."""
    def __init__(self, service: ServiceConfiguration, subject_pusher: SubjectPusher, integration_manager_subscriber: IntegrationManagerSubscriber):
        super().__init__(service_id="test.test_service", service=service, subject_pusher=subject_pusher, integration_manager_subscriber=integration_manager_subscriber)

    def initialize(self):
        """Initialize the service."""
        pass

    def start(self):
        """Start the service."""
        # simulate work
        for count in range(100):
            print(f"Demo service count: {count}")
            time.sleep(5)

    def stop(self):
        """Stop the service."""
        pass

    def restart(self):
        """Restart the service."""
        pass
