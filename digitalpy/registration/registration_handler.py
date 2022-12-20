import importlib
import os
from pathlib import PurePath
from typing import List
import pkg_resources

from abc import ABC, abstractmethod
from digitalpy.component.impl.default_facade import DefaultFacade
from digitalpy.config.configuration import Configuration
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
class RegistrationHandler(ABC):
    @abstractmethod
    @staticmethod
    def discover(entity_folder_path: PurePath) -> List[str]:
        """this method is used to discover all available entitys

        Args:
            entity_folder_path (str): the path in which to search for entitys. the searchable folder should be in the following format:\n
                entity_folder_path \n
                |-- some_entity \n
                |   `-- some_entity_facade.py\n
                `-- another_entity\n
                    `-- another_entity_facade.py\n
        Returns:
            List[str]: a list of available entitys in the given path
        """
        

    @abstractmethod
    @staticmethod
    def register(
        entity_path: PurePath, import_root: str, config: InifileConfiguration
    ) -> bool:
        """this method is used to register a given entity

        Args:
            entity_path (PurePath): the path to the directory of the entity to be registered.
            import_root (str): the import root from which to import the entitys facade.
            config (InifileConfiguration): the main configuration through which the entitys actions should be exposed.

        Returns:
            bool: whether or not the entity was registered successfully
        """
       

    @abstractmethod
    @staticmethod
    def save(manifest: Configuration, entity_name: str):
        """save a given entity to some form of persistency"""
        
    @abstractmethod
    @staticmethod
    def validate_manifest(manifest: Configuration, entity_name: str) -> bool:
        #TODO: determine better way to inform the caller that the manifest is invalid
        """validate that the entity is compatible with the current digitalpy version

        Args:
            manifest (Configuration): the manifest of a entity to be validated for this digitalpy installation
            entity_name (str): the name of the entity to be validated

        Raises:
            ValueError: raised if the manifest section is missing from the manifest configuration

        Returns:
            bool: whether the entity is compatible with the current digitalpy installation
        """
       