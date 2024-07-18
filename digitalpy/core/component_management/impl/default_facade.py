# pylint: disable=unused-argument
"""This is the default facade module. It is used to create a facade for a component. It is a simple example of a DigitalPyFacade.
"""
from types import ModuleType
from digitalpy.core.main.controller import Controller
from digitalpy.core.domain.node import Node
from digitalpy.core.parsing.load_configuration import LoadConfiguration
from digitalpy.core.digipy_configuration.impl.inifile_configuration import (
    InifileConfiguration,
)
from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.main.log_manager import LogManager
from digitalpy.core.main.impl.default_file_logger import DefaultFileLogger
from digitalpy.core.digipy_configuration.configuration import Configuration

from digitalpy.core.telemetry.tracer import Tracer


class DefaultFacade(Controller):
    def __init__(
        self,
        action_mapping_path: str,
        internal_action_mapping_path,
        logger_configuration,
        log_file_path,
        component_name=None,
        type_mapping=None,
        action_mapper: DefaultActionMapper = None,  # type: ignore
        base=ModuleType,
        request: Request = None,  # type: ignore
        response: Response = None,  # type: ignore
        configuration: Configuration = None,  # type: ignore
        configuration_path_template=None,
        tracing_provider_instance=None,
        manifest_path=None,
        **kwargs,
    ):
        """_summary_

        Args:
            action_mapping_path (str): path to the external action mapping of the application
            internal_action_mapping_path (str): path to the internal action mapping of the component
            logger_configuration (str): path to the ini file describing the configuration for the logger
            log_file_path (str): path to where the log files will be saved for this component
            component_name (str, optional): the name of this component. Defaults to the class name.
            type_mapping (str, optional): the path to the type mapping for this component if there is one
                type mapping maps a type to a action. Defaults to None.
            action_mapper (DefaultActionMapper, optional): the action mapper registered to the
                internal_action_mapping path, in other words, the internal action mapper. Defaults to None.
            base (package, optional): the package containing the base classes for the component,
                e.g. the component specific action mapper. Defaults to object.
            request (Request, optional): a request object to instantiate the facade with. Defaults to None.
            response (Response, optional): a response object to instantiate the facade with. Defaults to None.
            configuration (Configuration, optional):  . Defaults to None.
            configuration_path_template (string.Template, optional): a template defining the absoloute path to the model object definitions. Defaults to None.
            tracing_provider_instance (TracingProvider, optional): an instance of a digitalpy tracing provider used for logging. Defaults to None.
            manifest_path (str, optional): path to the component manifest file. Defaults to None.
        """
        super().__init__(
            action_mapper=action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )
        self.last_event = ""
        self.base = base

        self.action_mapping_path = action_mapping_path
        self.internal_action_mapping_path = internal_action_mapping_path
        self.type_mapping = type_mapping
        self.action_mapper = action_mapper
        if component_name is not None:
            self.component_name = component_name
        else:
            self.component_name = self.__class__.__name__

        # get a tracer from the tracer provider

        if tracing_provider_instance is not None:
            self.tracer: Tracer = tracing_provider_instance.create_tracer(
                self.component_name
            )
        else:
            self.tracer = None  # type: ignore
        # load the manifest file as a configuration
        if manifest_path is not None:
            self.manifest = InifileConfiguration("")
            self.manifest.add_configuration(manifest_path)

        # define the logging
        self.log_manager = LogManager()
        DefaultFileLogger.set_base_logging_path(log_file_path)
        self.log_manager.configure(
            DefaultFileLogger(
                name=self.component_name, config_file=logger_configuration
            )
        )
        self.logger = self.log_manager.get_logger()
        if configuration_path_template:
            self.config_loader = LoadConfiguration(configuration_path_template)
        else:
            self.config_loader = None

        self.injected_values = {
            "logger": self.logger,
            "config_loader": self.config_loader,
            "tracer": self.tracer,
        }

    def initialize(self, request, response):
        super().initialize(request, response)
        self.request.set_sender(self.__class__.__name__)

    def execute(self, method=None) -> None:
        self.request.set_value("logger", self.logger)
        self.request.set_value("config_loader", self.config_loader)
        self.request.set_value("tracer", self.tracer)
        if not method:
            return
        try:
            if hasattr(self, method):
                # pass all request values as keyword arguments
                getattr(self, method)(**self.request.get_values())
            else:
                response = self.execute_sub_action(self.request.get_action())
                # set all the values and senders in main response to the sub-response
                self.response.set_values(response.get_values())
                self.response.set_action(response.get_action())
                self.response.set_context(response.get_context())
                self.response.set_sender(response.get_sender())
        except Exception as e:
            self.logger.fatal(str(e))

        self.response.set_value("tracer", None)

    @staticmethod
    def public(func):
        """this method should be used as a decorator for
        facade methods being called directly. it's role is to
        inject internal attributes into the wrapped function which
        would generally be injected by the execute method"""

        def wrapper(self, *args, **kwargs):
            # ensure that required values are passed by to controller
            # methods even if method isnt called through .execute method
            kwargs.update(self.injected_values)

            return func(self, *args, **kwargs)

        return wrapper

    def get_logs(self, **kwargs):
        """get all the log files available"""
        return self.log_manager.get_logs()

    def discover(self, **kwargs):
        """discover the action mappings from the component"""
        config = InifileConfiguration(config_path=self.action_mapping_path)
        return config.config_array

    def register(self, config: InifileConfiguration, **kwargs):
        config.add_configuration(self.action_mapping_path)
        internal_config = InifileConfiguration("")
        internal_config.add_configuration(self.internal_action_mapping_path)
        ObjectFactory.register_instance(
            f"{self.component_name.lower()}actionmapper",
            self.base.ActionMapper(  # type: ignore
                ObjectFactory.get_instance("event_manager"),
                internal_config,
            ),
        )
        self._register_type_mapping()

    def unregister(self, config: InifileConfiguration, **kwargs):
        """unregister the component from the system"""
        ObjectFactory.clear_instance(f"{self.component_name.lower()}actionmapper")
        config.remove_configuration(self.action_mapping_path)

    def get_manifest(self, **kwargs):
        """returns the current manifest configuration"""
        return self.manifest

    def _register_type_mapping(self):
        """any component may or may not have a type mapping defined,
        if it does then it should be registered"""
        if self.type_mapping:
            request = ObjectFactory.get_new_instance("request")
            request.set_action("RegisterMachineToHumanMapping")
            request.set_value("machine_to_human_mapping", self.type_mapping)

            actionmapper = ObjectFactory.get_instance("SyncActionMapper")
            response = ObjectFactory.get_new_instance("response")
            actionmapper.process_action(request, response)

            request = ObjectFactory.get_new_instance("request")
            request.set_action("RegisterHumanToMachineMapping")
            # reverse the mapping and save the reversed mapping
            request.set_value(
                "human_to_machine_mapping", {k: v for v, k in self.type_mapping.items()}
            )

            actionmapper = ObjectFactory.get_instance("SyncActionMapper")
            response = ObjectFactory.get_new_instance("response")
            actionmapper.process_action(request, response)

    def accept_visitor(self, node: Node, visitor, **kwargs):
        return node.accept_visitor(visitor)

    def __setstate__(self, state: dict) -> None:
        from .. import base

        self.__dict__ = state
        if "base" in state:
            self.base = base

    def __getstate__(self) -> dict:
        tmp = self.__dict__
        set_base = tmp.get("base", None)
        if set_base is not None:
            tmp["base"] = True
        return tmp
