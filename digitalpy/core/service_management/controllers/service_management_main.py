from typing import Dict, List

from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.domain.service_status import ServiceStatus
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.service_management.controllers.service_management_process_controller import ServiceManagementProcessController
from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.service_management.domain.service_description import ServiceDescription
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.zmanager.response import Response


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

    def initialize_controllers(self):
        """This method is used to initialize the controllers once the service is started"""
        self.process_controller: ServiceManagementProcessController = ObjectFactory.get_instance("ServiceManagerProcessController")

    def start(self, object_factory: DefaultFactory, tracing_provider: TracingProvider):
        """This method is used to start the service"""
        super().start(object_factory=object_factory, tracing_provider=tracing_provider)
        self.initialize_connections("services")
        
    def stop(self):
        """This method is used to stop the service"""
        super().stop()

    def event_loop(self):
        """This method is used to run the service"""
        commands = self.listen_for_commands()

        for command in commands:
            self.handle_command(command)

    def handle_command(self, command: Response):
        """This method is used to handle a command"""

        if command.get_value("command") == "start_service":
            self.start_service(command.get_value("service_configuration"))
        elif command.get_value("command") == "stop_service":
            self.stop_service(command.get_value("service_id"))
        
    def listen_for_commands(self) -> List[Response]:
        """this method is responsible for waiting for the response, enabling
        the response to be sent by the main process responsible for sending
        CoT's. This handler simply returns an empty list in the case that there is no
        data to receive however if data is available from the /routing/response/
        topic it will be received parsed and returned so that it might be sent to
        all clients by the main loop
        """
        responses = self.broker_receive()
        return responses
    
    def initialize_service_description(self, service_configuration: Configuration) -> ServiceDescription:
        """This method is used to initialize a service description"""
        # construct the service description
        new_service_instance = ServiceDescription()

        # add the values from the configuration to the service description
        new_service_instance.name = service_configuration.get_value("name")
        new_service_instance.id = service_configuration.get_value("id")
        new_service_instance.protocol = service_configuration.get_value("protocol")
        new_service_instance.status = ServiceStatus.STOPPED
        new_service_instance.description = service_configuration.get_value("description")
        new_service_instance.start_time = None
        new_service_instance.last_message_time = None

        # add the service description to the service index
        self._service_index[new_service_instance.id] = new_service_instance

        return new_service_instance

    def start_service(self, service_configuration: Configuration):
        """This method is used to initialize the service process and start the service"""
        service_description = self.initialize_service_description(service_configuration)

        self.process_controller.start_process(service_description)
        # TODO: Add any additional logic or functionality as needed

    def stop_service(self, service_id: str):
        """This method is used to stop a service"""

    def _start_process(self, service_id: str):
        """This method is used to start a service process"""
