from typing import Dict, List
from digitalpy.core.component_management.impl.component_registration_handler import ComponentRegistrationHandler

from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.factory import Factory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.domain.service_status import ServiceStatus
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.service_management.controllers.service_management_process_controller import ServiceManagementProcessController
from digitalpy.core.service_management.digitalpy_service import DigitalPyService, COMMAND_PROTOCOL, COMMAND_ACTION
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
            protocol=COMMAND_PROTOCOL,
            network=None # type: ignore
        )

        # the service index is used to keep track of all registered services, their states, and their configurations
        self._service_index: Dict[str, ServiceDescription] = {}
        self.component_index: Dict[str, Configuration] = {}

    def initialize_controllers(self):
        """This method is used to initialize the controllers once the service is started"""
        self.process_controller: ServiceManagementProcessController = ObjectFactory.get_instance("ServiceManagerProcessController")

    def start(self, object_factory: DefaultFactory, tracing_provider: TracingProvider, component_index: Dict[str, Configuration]):
        """This method is used to start the service"""
        self.initialize_connections(COMMAND_PROTOCOL)
        self.component_index = component_index
        object_factory.clear_instance("servicemanager")
        super().start(object_factory=object_factory, tracing_provider=tracing_provider)
        
    def stop(self):
        """This method is used to stop the service"""
        super().stop()

    def event_loop(self):
        """This method is used to run the service"""
        commands = self.listen_for_commands()

        for command in commands:
            self.handle_command(command)

    def handle_exception(self, exception: Exception):

        #TODO: add logic to handle exceptions
        print(exception)

    def handle_command(self, command: Response):
        """This method is used to handle a command"""

        if command.get_value("command") == "start_service":
            self.start_service(command.get_value("target_service_id"))

        elif command.get_value("command") == "stop_service":
            self.stop_service(command.get_value("target_service_id"))

        elif command.get_value("command") == "restart_service":
            self.stop_service(command.get_value("target_service_id"))
            self.start_service(command.get_value("target_service_id"))

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
    
    def initialize_service_description(self, service_configuration: dict, service_id: str) -> ServiceDescription:
        """This method is used to initialize a service description"""
        # construct the service description
        new_service_instance = ServiceDescription()

        # set the id of the service
        new_service_instance.id = service_id

        # add the values from the configuration to the service description
        new_service_instance.name = str(service_configuration.get("name"))
        new_service_instance.protocol = str(service_configuration.get("protocol"))
        new_service_instance.network_interface = str(service_configuration.get("network"))
        new_service_instance.status = ServiceStatus.STOPPED
        new_service_instance.description = str(service_configuration.get("description"))
        new_service_instance.port = int(service_configuration.get("port")) # type: ignore
        new_service_instance.host = str(service_configuration.get("host"))

        # add the service description to the service index
        self._service_index[new_service_instance.id] = new_service_instance

        return new_service_instance

    def start_service(self, service_id: str):
        """This method is used to initialize the service process and start the service"""

        # check if the service is already running
        if self.is_service_running(service_id):
            return
        
        # parse the service id into the component name and the service name
        component_name, service_name = service_id.split(".")

        # get the configuration for the service
        service_component_configuration = self.component_index[component_name]

        # get the service configuration from the manifest of the component
        service_configuration = service_component_configuration.get_section(service_name)

        service_description = self.initialize_service_description(service_configuration, service_id)

        service_class = self.initialize_service_class(service_configuration, service_description)

        self.process_controller.start_process(service_description, service_class)

        service_description.status = ServiceStatus.RUNNING
        
    def is_service_running(self, service_id: str) -> bool:
        """This method is used to check if a service is running"""
        if service_id not in self._service_index:
            return False
        return self._service_index[service_id].status == ServiceStatus.RUNNING

    def initialize_service_class(self, service_configuration: dict, service_description: ServiceDescription):
        base_config: Configuration = ObjectFactory.get_instance("configuration")

        service_configuration.update(base_config.get_section("Service"))

        # initialize the service class
        service_class: DigitalPyService = ObjectFactory.get_instance(service_description.name, service_configuration)
        
        return service_class

    def stop_service(self, service_id: str):
        """This method is used to stop a service"""

        service_description = self._service_index[service_id]

        self._send_service_stop_request(service_id)

        self.process_controller.stop_process(service_description)

        service_description.status = ServiceStatus.STOPPED

    def _send_service_stop_request(self, service_id: str):
        req: Request = ObjectFactory.get_new_instance("Request")
        req.set_action(COMMAND_ACTION)
        req.set_context(service_id)
        req.set_value("command", "stop_service")
        req.set_value("target_service_id", service_id)
        req.set_format("pickled")
        self.subject_send_request(req, COMMAND_PROTOCOL, service_id)

    def _start_process(self, service_id: str):
        """This method is used to start a service process"""
