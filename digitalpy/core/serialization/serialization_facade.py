from digitalpy.core.component_management.impl.default_facade import DefaultFacade

from .controllers.xml_serialization_controller import XMLSerializationController
from .controllers.serialization_general_controller import SerializationGeneralController
from .configuration.serialization_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH
)
from . import base
class Serialization(DefaultFacade):
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

    def __init__(
            self,
            serialization_action_mapper,
            request,
            response,
            configuration,
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
                action_mapper=serialization_action_mapper,
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
                log_file_path=log_file_path
        )
        #self.deserialize = SerializationGeneralController()
        #self.serialize_to_file = SerializationGeneralController()
        #self.serialize = SerializationGeneralController()
        #self.domain_to_xml_parsing = SerializationGeneralController()
        #self.xml_to_domain_parsing = SerializationGeneralController()
        #self.domain_to_json_parsing = SerializationGeneralController()
        #self.domain_to_protobuf_parsing = SerializationGeneralController()
        #self.deserialize_from_file = SerializationGeneralController()
        self.xml_serializer = XMLSerializationController(request, response, serialization_action_mapper, configuration)
        self.general_serializer = SerializationGeneralController(request, response, serialization_action_mapper, configuration)

    def initialize(self, request, response):
        super().initialize(request, response)
        self.xml_serializer.initialize(request, response)
        self.general_serializer.initialize(request, response)

    def execute(self, method):
        self.request.set_value("logger", self.logger)
        self.request.set_value("config_loader", self.config_loader)
        self.request.set_value("tracer", self.tracer)
        try:
            if hasattr(self, method):
                getattr(self, method)(**self.request.get_values())
            else:
                response = self.execute_sub_action(self.request.get_action())
                self.response.set_values(response.get_values())
        except Exception as e:
            self.logger.fatal(str(e))

    def serialize_node_to_protocol(self, *args, **kwargs):
        """serialize a node to a given protocol
        """
        self.general_serializer.serialize_node_to_protocol(*args, **kwargs)
    