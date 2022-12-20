import importlib
import os
from pathlib import PurePath
from typing import List
import pkg_resources

from digitalpy.registration.registration_handler import RegistrationHandler
from digitalpy.component.impl.default_facade import DefaultFacade
from digitalpy.config.configuration import Configuration
from digitalpy.config.impl.inifile_configuration import InifileConfiguration

MANIFEST = "manifest"
DIGITALPY = "digitalpy"
REQUIRED_ALFA_VERSION = "requiredAlfaVersion"
NAME = "name"
VERSION = "version"
ID = "UUID"
VERSION_DELIMITER = "."


class ServiceRegistrationHandler(RegistrationHandler):
    """this class is used to manage service registration"""

    registered_services = {}

    @staticmethod
    def discover_services(service_folder_path: PurePath) -> List[str]:
        """this method is used to discover all available services

        Args:
            service_folder_path (str): the path in which to search for services. the searchable folder should be in the following format:\n
                service_folder_path \n
                |-- some_service \n
                |   `-- some_service_facade.py\n
                `-- another_service\n
                    `-- another_service_facade.py\n
        Returns:
            List[str]: a list of available services in the given path
        """
        potential_services = os.scandir(service_folder_path)
        services = []
        for potential_service in potential_services:
            facade_path = PurePath(
                potential_service.path, potential_service.name + ".py"
            )
            if os.path.exists(facade_path):
                services.append(PurePath(potential_service.path))
        return services

    @staticmethod
    def register_service(
        service_path: PurePath, import_root: str, config: InifileConfiguration
    ) -> bool:
        """this method is used to register a given service

        Args:
            service_path (PurePath): the path to the directory of the service to be registered.
            import_root (str): the import root from which to import the services facade.
            config (InifileConfiguration): the main configuration through which the services actions should be exposed.

        Returns:
            bool: whether or not the service was registered successfully
        """
        try:
            facade_path = PurePath(service_path, service_path.name + ".py")
            if os.path.exists(str(facade_path)):
                service_name = service_path.name.replace("_service", "")

                service = getattr(
                    importlib.import_module(
                        f"{import_root}.{service_path.name}.{service_name}"
                    ),
                    f"{''.join([name.capitalize() if name[0].isupper()==False else name for name in service_name.split('_')])}",
                )
                service_instance: DefaultFacade = service(
                    None, None, None, None
                )

                if ServiceRegistrationHandler.validate_manifest(
                    facade_instance.get_manifest(), service_name
                ):
                    facade_instance.register(config)
                else:
                    return False
            else:
                return False
            ServiceRegistrationHandler.save_service(facade_instance.get_manifest(), service_name)
            return True
        except Exception as e:
            # must use a print because logger may not be available
            print(f"failed to register service: {service_path}, with error: {e}")
            return False

    @staticmethod
    def save_service(manifest: Configuration, service_name: str):
        section = manifest.get_section(service_name + MANIFEST, include_meta=True)
        ServiceRegistrationHandler.registered_services[section[NAME]] = section

    @staticmethod
    def validate_manifest(manifest: Configuration, service_name: str) -> bool:
        #TODO: determine better way to inform the caller that the manifest is invalid
        """validate that the service is compatible with the current digitalpy version

        Args:
            manifest (Configuration): the manifest of a service to be validated for this digitalpy installation
            service_name (str): the name of the service to be validated

        Raises:
            ValueError: raised if the manifest section is missing from the manifest configuration

        Returns:
            bool: whether the service is compatible with the current digitalpy installation
        """
        # retrieve the current digitalpy version based on the setup.py
        digitalpy_version = pkg_resources.require(DIGITALPY)[0].version

        try:
            # get the manifest section from the configuration
            section = manifest.get_section(service_name + MANIFEST, include_meta=True)
        except ValueError:

            raise ValueError(
                f"manifest section missing, requires name {service_name+MANIFEST} please add the \
                following section to the manifest [{service_name+MANIFEST}], for more information on service\
                manifests please refer to the digitalpy documentation"
            )

        # validate the service name matches the name specified in the manifest
        if service_name != section[NAME]:
            return False

        # iterate the delimited version number and compare it to the digitalpy version
        for i in range(len(section[REQUIRED_ALFA_VERSION].split(VERSION_DELIMITER))):
            #check if the version matches
            digitalpy_version_number = digitalpy_version.split(VERSION_DELIMITER)[i] if len(digitalpy_version.split(VERSION_DELIMITER))>i else 0
            if int(digitalpy_version_number)>=int(section[REQUIRED_ALFA_VERSION].split(VERSION_DELIMITER)[i]):
                continue
            else:
                return False
            
        # dont approve the manifest if the service has already been registered
        if (
            service_name in ServiceRegistrationHandler.registered_services
            and section[VERSION]
            != ServiceRegistrationHandler.registered_services[service_name][VERSION]
        ):
            return False

        # dont approve the manifest if a service with the same name but a different ID already exists
        if (
            service_name in ServiceRegistrationHandler.registered_services
            and ServiceRegistrationHandler.registered_services[service_name][ID]
            != section[ID]
        ):
            return False

        return True
