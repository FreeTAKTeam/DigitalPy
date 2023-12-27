"""
The Service Management component in DigitalPy is a core function designed 
to manage the lifecycle and operations of various services within the framework. 
It provides abstract capabilities for installing, deinstalling, discovering, starting, 
and stopping services, aligning with the principles set in the Network component for network 
type and communication protocols.

The ServiceManager Service manages the following responsibilities:
* Lifecycle Management:
    Installation and Deinstallation: Allows for the installation and removal 
    of services within the DigitalPy environment.
    
* Service Discovery: Facilitates the discovery of available services, aiding 
  in dynamic service management and integration.
    Start/Stop Mechanisms: Provides the ability to start and stop services 
    dynamically, ensuring flexibility and responsiveness in resource 
    management.

* Service Isolation and Association:
    Ensures each service runs in a thread and  is isolated from others, 
    Associates each service with a specific port and network type, as defined 
    in the Network component.
    Supports various data formats and protocols such as XML, JSON, Protobuf, 
    etc.
"""

from datetime import datetime
from typing import Any, Dict, List

from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.service_management.domain.service_manager_operations \
    import ServiceManagerOperations
from digitalpy.core.service_management.domain.service_operations import ServiceOperations
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.domain.service_status import ServiceStatus
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.service_management.controllers.service_management_process_controller \
    import ServiceManagementProcessController
from digitalpy.core.service_management.digitalpy_service \
    import DigitalPyService, COMMAND_PROTOCOL, COMMAND_ACTION
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.service_management.domain.service_description import ServiceDescription
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.zmanager.response import Response
from digitalpy.core.domain.domain.service_health import ServiceHealth
from digitalpy.core.health.domain.service_health_category import ServiceHealthCategory


class ServiceManagementMain(DigitalPyService):
    """The Service Management component in DigitalPy is a core function designed 
    to manage the lifecycle and operations of various services within the framework. 
    It provides abstract capabilities for installing, deinstalling, discovering, starting, 
    and stopping services, aligning with the principles set in the Network component for network 
    type and communication protocols."""

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
            network=None  # type: ignore
        )

        # the service index is used to keep track of all registered services,
        # their states, and their configurations
        self._service_index: Dict[str, ServiceDescription] = {}
        self.component_index: Dict[str, Configuration] = {}
        self.process_controller: ServiceManagementProcessController

    def initialize_controllers(self):
        """
        Initializes the controllers for service management.
        """
        self.process_controller: ServiceManagementProcessController = ObjectFactory.get_instance(
            "ServiceManagerProcessController")

    def stop(self):
        """
        This method is used to stop the service manager.
        """
        self.stop_all_services()
        raise SystemExit

    def stop_all_services(self):
        """This method is used to stop all services managed by the service manager"""
        for service_id in self._service_index:
            self.stop_service(service_id)

    def start(self, object_factory: DefaultFactory, tracing_provider: TracingProvider,
              component_index: Dict[str, Configuration]):
        """This method is used to start the service

        Args:
            object_factory (DefaultFactory): 
                The object factory used for dependency injection.
            tracing_provider (TracingProvider): 
                The tracing provider used for logging and monitoring.
            component_index (Dict[str, Configuration]): 
                The index of components and their configurations.

        Returns:
            None
        """
        self.initialize_connections(COMMAND_PROTOCOL)
        self.component_index = component_index
        object_factory.clear_instance("servicemanager")

        ObjectFactory.configure(object_factory)
        self.tracer = tracing_provider.create_tracer(self.service_id)
        self.initialize_controllers()
        self.initialize_connections(self.protocol)

        self.install_all_services()

        self.status = ServiceStatus.RUNNING
        # member exists in parent class
        self.execute_main_loop()  # pylint: disable=no-member

    def event_loop(self):
        """This method is used to run the service"""
        commands = self.listen_for_commands()

        for command in commands:
            self.handle_command(command)

    def install_all_services(self):
        """
        Discover and install all services defined in the component manifest.

        This method iterates over the component index and retrieves the configuration
        for each component. It then discovers services from the component
        manifest. Finally it starts the services that have a default status of "RUNNING".

        Returns:
            None
        """
        for component_name in self.component_index:
            component_configuration = self.component_index[component_name]

            # TODO: The service definitions should be moved out of the component manifest
            # for better organization and separation of concerns.
            for service_name in component_configuration.get_sections():
                if not service_name.endswith("Service"):
                    continue

                service_config = component_configuration.get_section(
                    service_name)
                if service_config.get("default_status", ServiceStatus.STOPPED) \
                        == ServiceStatus.RUNNING.value:
                    service_id = str(service_config.get("service_id"))
                    self.start_service(service_id)

    def handle_exception(self, exception: Exception):
        """This method is used to handle an exception"""
        # TODO: add logic to handle exceptions
        print(exception)

    def handle_command(self, command: Response):
        """This method is used to handle a command, commands are typically sent from the DigitalPy 
        application core through the ZManager"""

        if command.get_value("command") == str(ServiceManagerOperations.START_SERVICE.value):
            self.start_service(command.get_value("target_service_id"))

        elif command.get_value("command") == str(ServiceManagerOperations.STOP_SERVICE.value):
            self.stop_service(command.get_value("target_service_id"))

        elif command.get_value("command") == str(ServiceManagerOperations.RESTART_SERVICE.value):
            self.stop_service(command.get_value("target_service_id"))
            self.start_service(command.get_value("target_service_id"))

        elif command.get_value("command") == str(ServiceManagerOperations.GET_ALL_SERVICE_HEALTH.value):
            all_service_health = self.get_all_service_health()
            self.send_response_to_core(all_service_health, command.get_id())

    def send_response_to_core(self, message: Any, command_id: str):
        """This method is used to send a response to the DigitalPy application core"""
        from digitalpy.core.main.DigitalPy import DigitalPy  # pylint: disable=import-outside-toplevel
        resp = ObjectFactory.get_new_instance("Response")
        resp.set_value("message", message)
        resp.set_action("publish")
        resp.set_format("pickled")
        resp.set_id(command_id)
        self.subject_send_request(
            resp, COMMAND_PROTOCOL, DigitalPy.service_id)

    def get_all_service_health(self):
        """This method is used to get the health of all services"""
        service_health = {}
        for service_id, service_desc in self._service_index.items():
            if service_desc.status == ServiceStatus.RUNNING:
                service_health[service_id] = self.get_service_health(
                    service_id)

        return service_health

    def get_service_health(self, service_id: str):
        """This method is used to get the health of a service"""
        req: Request = ObjectFactory.get_new_instance("Request")
        req.set_action(COMMAND_ACTION)
        req.set_context(service_id)
        req.set_value("command", str(ServiceOperations.GET_HEALTH.value))
        req.set_value("target_service_id", service_id)
        req.set_format("pickled")
        self.subject_send_request(req, COMMAND_PROTOCOL, service_id)
        resp = self.broker_receive_response(request_id=req.get_id(), timeout=5)

        if resp is None:
            service_health: ServiceHealth = ServiceHealth()
            service_health.status = ServiceHealthCategory.UNRESPONSIVE
            service_health.service_id = service_id
            service_health.timestamp = datetime.now()

        else:
            service_health = resp.get_value("message")

        return service_health

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

    def initialize_service_description(self, service_configuration: dict,
                                       service_id: str) -> ServiceDescription:
        """This method is used to initialize a service description"""
        # construct the service description
        new_service_instance = ServiceDescription()

        # set the id of the service
        new_service_instance.id = service_id

        # add the values from the configuration to the service description
        new_service_instance.name = str(service_configuration.get("name"))
        new_service_instance.protocol = str(
            service_configuration.get("protocol"))
        new_service_instance.network_interface = str(
            service_configuration.get("network"))
        new_service_instance.status = ServiceStatus.STOPPED
        new_service_instance.description = str(
            service_configuration.get("description"))
        new_service_instance.port = int(
            service_configuration.get("port"))  # type: ignore
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
        service_configuration = service_component_configuration.get_section(
            service_name)

        # initialize the service description
        service_description = self.initialize_service_description(
            service_configuration, service_id)

        # initialize the service class
        service_class = self.initialize_service_class(
            service_configuration, service_description)

        # start the service process
        self.process_controller.start_process(
            service_description, service_class)

        # update the status of the service
        service_description.status = ServiceStatus.RUNNING

    def is_service_running(self, service_id: str) -> bool:
        """This method is used to check if a service is running"""

        # if the service is not in the service index then it is not running
        if service_id not in self._service_index:
            return False
        # if the service is in the service index and the status is running
        # then the service is running, otherwise it is not running.
        return self._service_index[service_id].status == ServiceStatus.RUNNING

    def initialize_service_class(self, service_configuration: dict,
                                 service_description: ServiceDescription) -> DigitalPyService:
        """This method is used to initialize a service class

        Args:
            service_configuration (dict): 
                The configuration settings for the service. This is a dictionary that contains
                key-value pairs of configuration settings.
            service_description (ServiceDescription): 
                An object that describes the service. This includes properties like the name of the service, 
                its version, and other metadata.

        Returns:
            DigitalPyService: an initialized digitalpy service object
        """
        base_config: Configuration = ObjectFactory.get_instance(
            "configuration")

        service_configuration.update(base_config.get_section("Service"))

        # initialize the service class
        service_class: DigitalPyService = ObjectFactory.get_instance(
            service_description.name, service_configuration)

        return service_class

    def stop_service(self, service_id: str):
        """
        This method is used to stop a service.

        Args:
            service_id (str): The ID of the service to stop.

        Notes:
            - If the specified service ID matches the ID of the current service, the `stop()` 
                method will be called to handle a system shutdown.
            - The method will send a service stop request using the `_send_service_stop_request()` 
                method.
            - The `stop_process()` method of the process controller will be called to stop the 
                service process.
            - The status of the service will be updated to `ServiceStatus.STOPPED`.
        """
        if service_id.lower() == self.service_id.lower():
            self.stop()

        service_description = self._service_index[service_id]

        self._send_service_stop_request(service_id)

        self.process_controller.stop_process(service_description)

        service_description.status = ServiceStatus.STOPPED

    def _send_service_stop_request(self, service_id: str):
        """
        This method is used to send a service stop request to the service. this method is used
        internally as a helper method for the `stop_service()` method.

        Args:
            service_id (str): The ID of the service to stop.
        """
        req: Request = ObjectFactory.get_new_instance("Request")
        req.set_action(COMMAND_ACTION)
        req.set_context(service_id)
        req.set_value("command", str(ServiceOperations.STOP.value))
        req.set_value("target_service_id", service_id)
        req.set_format("pickled")
        self.subject_send_request(req, COMMAND_PROTOCOL, service_id)
