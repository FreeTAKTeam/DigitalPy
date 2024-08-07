from digitalpy.core.service_management.controllers.service_management_controller import ServiceManagementController
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.main.object_factory import ObjectFactory

from .controllers.service_management_sender_controller import (
    ServiceManagementSenderController,
)
from .configuration.service_management_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH,
)
from . import base


class ServiceManagement(DefaultFacade):
    """Facade class for the this component. Responsible for handling all public
    routing. Forwards all requests to the internal router.
      WHY
      <ul>
        <li><b>Isolation</b>: We can easily isolate our code from the complexity of
    a subsystem.</li>
        <li><b>Testing Process</b>: Using Facade Method makes the process of testing
    comparatively easy since it has convenient methods for common testing tasks.
    </li>
        <li><b>Loose Coupling</b>: Availability of loose coupling between the
    clients and the Subsystems.</li>
      </ul>
    """

    # default constructor  def __init__(self):

    def __init__(
        self,
        service_management_action_mapper,
        request,
        response,
        configuration,
        persistence_path: str = None,
        log_file_path: str = LOG_FILE_PATH,
    ):
        super().__init__(
            # the path to the external action mapping
            action_mapping_path=ACTION_MAPPING_PATH,
            # the path to the internal action mapping
            internal_action_mapping_path=INTERNAL_ACTION_MAPPING_PATH,
            # the path to the logger configuration
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            # the package containing the base classes
            base=base,
            # the component specific action mapper (passed by constructor)
            action_mapper=service_management_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
            # the template for the absolute path to the model object definitions
            configuration_path_template=CONFIGURATION_PATH_TEMPLATE,
            # the path to the manifest file
            manifest_path=MANIFEST_PATH,
            # the path for log files to be stored
            log_file_path=log_file_path,
        )
        # instantiating the sync_action_mapper for use by the service management sender controller to call external
        sync_action_mapper = ObjectFactory.get_instance("syncactionmapper")
        self.sender_controller = ServiceManagementSenderController(
            request,
            response,
            service_management_action_mapper,
            sync_action_mapper,
            configuration,
        )
        self.service_management_controller = ServiceManagementController(
            request, response, service_management_action_mapper, configuration
        )

    def initialize(self, request, response):
        self.request = request
        self.response = response
        self.sender_controller.initialize(request, response)

    def execute(self, method):
        self.request.set_value("logger", self.logger)
        self.request.set_value("config_loader", self.config_loader)
        self.request.set_value("tracer", self.tracer)
        try:
            if hasattr(self, method):
                getattr(self, self.request.get_action())(**self.request.get_values())
            else:
                response = self.execute_sub_action(self.request.get_action())
                self.response.set_values(response.get_values())
        except Exception as e:
            self.logger.fatal(str(e))

    def publish(self, *args, **kwargs):
        self.sender_controller.publish(*args, **kwargs)

    @DefaultFacade.public
    def initialize_service(self, *args, **kwargs):
        """This method is used to initialize the service to its default state and register it with the service management core"""
        self.service_management_controller.initialize_service(*args, **kwargs)

    @DefaultFacade.public
    def start_service(self, *args, **kwargs):
        """This method is used to initialize the service process and start the service"""
        self.service_management_controller.start_service(*args, **kwargs)
                                                         
    @DefaultFacade.public
    def stop_service(self, *args, **kwargs):
        """This method is used to stop the service process"""
        self.service_management_controller.stop_service(*args, **kwargs)
    @DefaultFacade.public
    def restart_service(self, *args, **kwargs):
        """This method is used to restart the service process"""
        self.service_management_controller.restart_service(*args, **kwargs)
    @DefaultFacade.public
    def get_service_status(self, *args, **kwargs):
        """This method is used to get the status of the service"""
