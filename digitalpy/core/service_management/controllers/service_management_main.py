from typing import Dict

from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.service_management.controllers.service_management_process_controller import ServiceManagementProcessController
from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.service_management.domain.service_description import ServiceDescription
from digitalpy.core.digipy_configuration.configuration import Configuration


class ServiceManagementMain(DigitalPyService):
    # TODO: this class' description should come from the ASOT
    """"""

    def __init__(
        self,
        service_id: str,
        subject_address: str,
        subject_port: int,
        subject_protocol: str,
        integration_manager_address: str,
        integration_manager_port: int,
        integration_manager_protocol: str,
        formatter: Formatter,
    ):
        """constructor for the ServiceManagementMain class

        Args:
            subject_address (str): the address of the zmanager "subject"
            subject_port (int): the port of the zmanager "subject"
            integration_manager_address (str): the address of the zmanager "integration_manager"
            integration_manager_port (int): the port of the zmanager "integration_manager"
            formatter (Formatter): _description_
        """
        super().__init__(
            service_id,
            subject_address,
            subject_port,
            subject_protocol,
            integration_manager_address,
            integration_manager_port,
            integration_manager_protocol,
            formatter,
        )

        # the service index is used to keep track of all registered services, their states, and their configurations
        self._service_index: Dict[str, ServiceDescription] = {}

    def start(self, object_factory: DefaultFactory, tracing_provider: TracingProvider):
        """This method is used to start the service"""
        super().start(object_factory=object_factory, tracing_provider=tracing_provider)

    def stop(self):
        """This method is used to stop the service"""
        super().stop()

    def event_loop(self):
        """This method is used to run the service"""
        command = self.listen_for_commands()
        
    def listen_for_commands(self):
        """This method is used to listen for commands from the integration manager"""
        

    def begin_service(self, service_configuration: Configuration):
        """This method is used to initialize the service process and start the service"""
        new_service_instance = ServiceDescription()

        # TODO: Implement the logic to initialize the service process and start the service

        # Example code:
        # self._service_index[new_service_instance.service_id] = new_service_instance
        # new_service_instance.start()

        # TODO: Add any additional logic or functionality as needed

    def _start_process(self, service_id: str):
        """This method is used to start a service process"""
