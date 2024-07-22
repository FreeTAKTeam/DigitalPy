from digitalpy.core.component_management.controllers.component_management_persistence_controller_impl import (
    Component_managementPersistenceControllerImpl,
)
from .controllers.component_management_persistence_controller_impl import (
    Component_managementPersistenceControllerImpl,
)
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.zmanager.impl.async_action_mapper import AsyncActionMapper
from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from .controllers.component_management_controller_impl import (
    Component_managementControllerImpl,
)
from .configuration.component_management_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH,
)

from . import base


class ComponentManagement(DefaultFacade):
    """ """

    def __init__(
        self,
        sync_action_mapper: DefaultActionMapper,
        request: Request,
        response: Response,
        configuration,
        action_mapper: AsyncActionMapper = None,  # type: ignore
        tracing_provider_instance=None,
    ):  # type: ignore
        super().__init__(
            # the path to the external action mapping
            action_mapping_path=str(ACTION_MAPPING_PATH),
            # the path to the internal action mapping
            internal_action_mapping_path=str(INTERNAL_ACTION_MAPPING_PATH),
            # the path to the logger configuration
            logger_configuration=str(LOGGING_CONFIGURATION_PATH),
            # the package containing the base classes
            base=base,  # type: ignore
            # the general action mapper (passed by constructor)
            action_mapper=sync_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
            # log file path
            log_file_path=LOG_FILE_PATH,
            # the tracing provider used
            tracing_provider_instance=tracing_provider_instance,
            # the template for the absolute path to the model object definitions
            configuration_path_template=CONFIGURATION_PATH_TEMPLATE,
            # the path to the manifest file
            manifest_path=str(MANIFEST_PATH),
        )
        self.persistence_controller = Component_managementPersistenceControllerImpl(
            request, response, sync_action_mapper, configuration
        )
        self.component_management_controller = Component_managementControllerImpl(
            request, response, sync_action_mapper, configuration
        )

    def initialize(self, request, response):
        self.component_management_controller.initialize(request, response)
        self.persistence_controller.initialize(request, response)

        return super().initialize(request, response)

    def execute(self, method=None):
        try:
            if hasattr(self, method):  # type: ignore
                print("executing method " + str(method))  # type: ignore
                getattr(self, method)(**self.request.get_values())  # type: ignore
            else:
                self.request.set_value("logger", self.logger)
                self.request.set_value("config_loader", self.config_loader)
                self.request.set_value("tracer", self.tracer)
                response = self.execute_sub_action(self.request.get_action())
                self.response.set_values(response.get_values())
        except Exception as e:
            self.logger.fatal(str(e))

    @DefaultFacade.public
    def GETPullComponent(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.PullComponent(*args, **kwargs)

    @DefaultFacade.public
    def POSTComponentRequiredAlfaVersion(self, *args, **kwargs):
        """ """
        self.component_management_controller.POSTComponentRequiredAlfaVersion(
            *args, **kwargs
        )

    @DefaultFacade.public
    def POSTInstallAllComponents(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.POSTInstallAllComponents(*args, **kwargs)

    @DefaultFacade.public
    def DELETEComponent(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.DELETEComponent(*args, **kwargs)

    @DefaultFacade.public
    def POSTComponent(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.POSTComponent(*args, **kwargs)

    @DefaultFacade.public
    def GETComponent(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.GETComponent(*args, **kwargs)

    @DefaultFacade.public
    def PATCHComponent(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.PATCHComponent(*args, **kwargs)

    @DefaultFacade.public
    def GETComponentId(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.GETComponentId(*args, **kwargs)

    @DefaultFacade.public
    def GETComponentStatus(self, *args, **kwargs):
        """returns the status of the component or the last error"""
        self.component_management_controller.GETComponentStatus(*args, **kwargs)

    @DefaultFacade.public
    def POSTActionKey(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.POSTActionKey(*args, **kwargs)

    @DefaultFacade.public
    def DELETEActionKey(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.DELETEActionKey(*args, **kwargs)

    @DefaultFacade.public
    def GETActionKey(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.GETActionKey(*args, **kwargs)

    @DefaultFacade.public
    def PATCHActionKey(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.PATCHActionKey(*args, **kwargs)

    @DefaultFacade.public
    def GETComponentRegister(self, *args, **kwargs):
        """register a component"""
        self.component_management_controller.GETComponentRegister(*args, **kwargs)

    @DefaultFacade.public
    def GETComponentDiscovery(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.GETComponentDiscovery(*args, **kwargs)

    @DefaultFacade.public
    def GETActionKeyId(self, *args, **kwargs):
        """TODO"""
        self.component_management_controller.GETActionKeyId(*args, **kwargs)
