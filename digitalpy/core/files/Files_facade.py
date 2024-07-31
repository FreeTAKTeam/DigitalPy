from digitalpy.core.files.controllers.files_controller_impl import FilesControllerImpl
from digitalpy.core.files.domain.model.file import File
from .controllers.Files_persistence_controller import FilesPersistenceController
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.zmanager.impl.async_action_mapper import AsyncActionMapper
from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from .controllers.files_controller import FilesController
from .configuration.Files_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH
)

from . import base


class Files(DefaultFacade):
    """
    """

    def __init__(self, sync_action_mapper: DefaultActionMapper, request: Request,
                 response: Response, configuration,
                 action_mapper: AsyncActionMapper = None,  # type: ignore
                 tracing_provider_instance=None):  # type: ignore
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
        self.persistence_controller = FilesPersistenceController(
            request, response, sync_action_mapper, configuration)
        self.Files_controller = FilesControllerImpl(
            request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        self.Files_controller.initialize(request, response)
        self.persistence_controller.initialize(request, response)

        return super().initialize(request, response)

    def execute(self, method=None):
        try:
            if hasattr(self, method):  # type: ignore
                print("executing method "+str(method))  # type: ignore
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
    def get_or_create_file(self, *args, **kwargs) -> File:
        """get a file from the filesystem based on the specified path or create a new file if one does not yet exist.
        """
        return self.Files_controller.get_or_create_file(*args, **kwargs)
    @DefaultFacade.public
    def get_or_create_folder(self, *args, **kwargs):
        """get a folder from the filesystem based on the specified path or create a new folder if one does not yet exist.
        """
        self.Files_controller.get_or_create_folder(*args, **kwargs)
    @DefaultFacade.public
    def get_folder(self, *args, **kwargs):
        """get a folder based on the specified path
        """
        self.Files_controller.get_folder(*args, **kwargs)
    @DefaultFacade.public
    def create_folder(self, *args, **kwargs):
        """create a new folder in the file system at the specified path
        """
        self.Files_controller.create_folder(*args, **kwargs)
    @DefaultFacade.public
    def delete_folder(self, *args, **kwargs):
        """delete the given folder instance.
        """
        self.Files_controller.delete_folder(*args, **kwargs)
    @DefaultFacade.public
    def get_file(self, *args, **kwargs) -> File:
        """get a file from the file system based on the specified path
        """
        return self.Files_controller.get_file(*args, **kwargs)
    @DefaultFacade.public
    def create_file(self, *args, **kwargs):
        """create a new file in the filesystem at the specified path.
        """
        self.Files_controller.create_file(*args, **kwargs)
    @DefaultFacade.public
    def delete_file(self, *args, **kwargs):
        """delete the file at the specified path
        """
        self.Files_controller.delete_file(*args, **kwargs)
