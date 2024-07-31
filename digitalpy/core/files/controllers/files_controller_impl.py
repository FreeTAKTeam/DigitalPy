"""
This is the main controller class of the application. Every operation of the controller is realized by this file
OOTB. It is recommended that you (the developper) avoid adding further methods to the file and instead add supporting
controllers with these methods should you need them. This controller is called directly by the facade in order to
fulfil any requests made to the component by default.
"""

from typing import TYPE_CHECKING
from pathlib import Path


from .files_controller import FilesController

# import builders
from digitalpy.core.files.domain.builder.file_builder_impl import FileBuilderImpl
from digitalpy.core.files.domain.builder.folder_builder import FolderBuilder

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient
    from digitalpy.core.files.domain.model.folder import Folder
    from digitalpy.core.files.domain.model.file import File
    from digitalpy.core.files.domain.model.error import Error

class FilesControllerImpl(FilesController):

    def __init__(self, request: 'Request',
                 response: 'Response',
                 sync_action_mapper: 'DefaultActionMapper',
                 configuration: 'Configuration'):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.Folder_builder = FolderBuilder(request, response, sync_action_mapper, configuration)
        self.File_builder = FileBuilderImpl(request, response, sync_action_mapper, configuration)

    def initialize(self, request: 'Request', response: 'Response'):
        """This function is used to initialize the controller. 
        It is intiated by the service manager."""
        self.Folder_builder.initialize(request, response)
        self.File_builder.initialize(request, response)
        self.Error_builder.initialize(request, response)
        self.Files_persistence_controller.initialize(request, response)
        return super().initialize(request, response)
    
    def get_or_create_file(self, path: 'str', config_loader, *args, **kwargs) -> 'File' : # pylint: disable=unused-argument
        """get a file from the filesystem based on the specified path or create a new file if one does not yet exist."""
        path_obj = Path(path)
        if not path_obj.exists():
            return self.create_file(path, config_loader)
        else:
            return self.get_file(path, config_loader)

    def get_or_create_folder(self, path: 'str', client: 'NetworkClient', config_loader, *args, **kwargs) -> 'Folder' : # pylint: disable=unused-argument
        """get a folder from the filesystem based on the specified path or create a new folder if one does not yet exist."""
        return None

    def get_folder(self, path: 'str', client: 'NetworkClient', config_loader, *args, **kwargs) -> 'Folder' : # pylint: disable=unused-argument
        """get a folder based on the specified path"""
        return None

    def create_folder(self, path: 'str', client: 'NetworkClient', config_loader, *args, **kwargs) -> 'Folder' : # pylint: disable=unused-argument
        """create a new folder in the file system at the specified path"""
        return None

    def delete_folder(self, recursive: 'str', client: 'NetworkClient', config_loader, *args, **kwargs): # pylint: disable=unused-argument
        """delete the given folder instance."""
        return None

    def get_file(self, path: 'str', config_loader, *args, **kwargs) -> 'File' : # pylint: disable=unused-argument
        """get a file from the file system based on the specified path"""
        path_obj = Path(path)
        if path_obj.exists():
            self.File_builder.build_empty_object(config_loader=config_loader)
            self.File_builder.add_object_data(path_obj)
            return self.File_builder.get_result()
        else:
            raise FileNotFoundError(f"File {path} not found")

    def create_file(self, path: 'str', config_loader, *args, **kwargs) -> 'File' : # pylint: disable=unused-argument
        """create a new file in the filesystem at the specified path."""
        path_obj = Path(path)
        if path_obj.exists():
            raise FileExistsError(f"File {path} already exists")
        
        path_obj.touch()
        self.File_builder.build_empty_object(config_loader=config_loader)
        self.File_builder.add_object_data(path_obj)
        return self.File_builder.get_result()

    def delete_file(self, client: 'NetworkClient', config_loader, *args, **kwargs): # pylint: disable=unused-argument
        """delete the file at the specified path"""
        return None

