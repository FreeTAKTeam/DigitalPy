from io import TextIOBase
from typing import TYPE_CHECKING
from pathlib import PurePath

import pkg_resources

from digitalpy.core.component_management.configuration.component_management_constants import (
    DIGITALPY,
    MANIFEST,
    NAME,
    REQUIRED_ALFA_VERSION,
    VERSION_DELIMITER,
)

from digitalpy.core.digipy_configuration.impl.inifile_configuration import (
    InifileConfiguration,
)


from digitalpy.core.main.controller import Controller

# import builders
from digitalpy.core.component_management.domain.builder.component_builder import (
    ComponentBuilder,
)
from digitalpy.core.component_management.domain.builder.error_builder import (
    ErrorBuilder,
)
from digitalpy.core.main.object_factory import ObjectFactory
from .component_management_persistence_controller import (
    Component_ManagementPersistenceController,
)
if TYPE_CHECKING:
    from digitalpy.core.component_management.impl.default_facade import DefaultFacade
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient
    
    from digitalpy.core.component_management.domain.model.error import Error


class ComponentManifestController(Controller):
    """This controller is responsible for managing the component manifest files.
    """

    def __init__(
        self,
        request: "Request",
        response: "Response",
        sync_action_mapper: "DefaultActionMapper",
        configuration: "Configuration",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.Component_builder = ComponentBuilder(
            request, response, sync_action_mapper, configuration
        )
        self.Error_builder = ErrorBuilder(
            request, response, sync_action_mapper, configuration
        )
        self.Component_Management_persistence_controller = (
            Component_ManagementPersistenceController(
                request, response, sync_action_mapper, configuration
            )
        )

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller.
        It is intiated by the service manager."""
        self.Component_builder.initialize(request, response)
        self.Error_builder.initialize(request, response)
        self.Component_Management_persistence_controller.initialize(request, response)
        return super().initialize(request, response)

    def read_manifest(self, stream: TextIOBase) -> dict:
        """this method is used to read a component's manifest
        
        Args:
            path (PurePath): the path to the manifest file
        
        Returns:
            dict: the manifest configuration
        """
        manifest = InifileConfiguration("")
        result = {}
        manifest.parse_ini_stream(result, stream)
        # return only the contents of the first section
        return list(result.values())[0]
    
    def validate_manifest(
        self, manifest: InifileConfiguration, component_name: "str"
    ) -> "bool":
        """this method is used to validate a component's manifest

        Args:
            manifest (dict): the manifest to validate
            component_name (str): the name of the component
            facade_instance (DefaultFacade): the facade instance of the component

        Returns:
            bool: whether the manifest is valid
        """

        try:
            # get the manifest section from the configuration
            section = manifest.get_section(component_name + MANIFEST, include_meta=True)
        except ValueError as exc:

            raise ValueError(
                f"manifest section missing, requires name {component_name+MANIFEST} please add the\
                following section to the manifest [{component_name+MANIFEST}], for more information\
                on component manifests please refer to the digitalpy documentation"
            ) from exc

        # validate the component name matches the name specified in the manifest
        if component_name != section[NAME]:
            return False

        if not self.check_version(section[REQUIRED_ALFA_VERSION]):
            return False

        return True

    def check_version(self, required_version: "str") -> "bool":
        """this method is used to check the version of the component

        Args:
            version (str): the version to check

        Returns:
            bool: True if the version is valid, False otherwise
        """
        # retrieve the current digitalpy version based on the setup.py
        digitalpy_version = pkg_resources.require(DIGITALPY)[0].version
        required_version_sections = required_version.split(VERSION_DELIMITER)
        # iterate the delimited version number and compare it to the digitalpy version
        for i, _ in enumerate(required_version_sections):
            # check if the version matches
            digitalpy_version_number = (
                digitalpy_version.split(VERSION_DELIMITER)[i]
                if len(digitalpy_version.split(VERSION_DELIMITER)) > i
                else 0
            )
            if int(digitalpy_version_number) > int(required_version_sections[i]):
                break
            elif int(digitalpy_version_number) == int(required_version_sections[i]):
                continue
            else:
                return False
        return True
