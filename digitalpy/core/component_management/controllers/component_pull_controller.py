from typing import TYPE_CHECKING
import requests

from digitalpy.core.component_management.configuration.component_management_constants import COMPONENT_DOWNLOAD_PATH
from digitalpy.core.component_management.controllers.component_manifest_controller import ComponentManifestController

from digitalpy.core.component_management.domain.builder.component_builder_impl import ComponentBuilderImpl
from digitalpy.core.main.controller import Controller

# import builders
from .component_management_persistence_controller_impl import (
    Component_managementPersistenceControllerImpl,
)


if TYPE_CHECKING:
    from digitalpy.core.component_management.impl.default_facade import DefaultFacade
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient
    
    from digitalpy.core.component_management.domain.model.error import Error


class ComponentPullController(Controller):
    """This controller is responsible for pulling components from remote datasources.
    """

    def __init__(
        self,
        request: "Request",
        response: "Response",
        sync_action_mapper: "DefaultActionMapper",
        configuration: "Configuration",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.Component_builder = ComponentBuilderImpl(
            request, response, sync_action_mapper, configuration
        )
        self.Component_Management_persistence_controller = (
            Component_managementPersistenceControllerImpl(
                request, response, sync_action_mapper, configuration
            )
        )
        self.component_manifest_controller = ComponentManifestController(
            request, response, sync_action_mapper, configuration
        )

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller.
        It is intiated by the service manager."""
        self.Component_builder.initialize(request, response)
        self.Component_Management_persistence_controller.initialize(request, response)
        return super().initialize(request, response)

    def pull_component_http(self, url: str, config_loader, *args, **kwargs) -> str:
        """This function is used to pull a component from a git repository.

        Args:
            url (str): The URL of the git repository.
            client (NetworkClient): The network client to use.
            config_loader: The configuration loader to use.
    
        Raises:
            Exception: If the component could not be pulled
        
        Returns:
            str: The path to the pulled component.
        """
        r = requests.get(url, stream=True, timeout=10)

        if r.status_code != 200:
            raise requests.exceptions.RequestException("Failed to pull component")
        
        with open(str(COMPONENT_DOWNLOAD_PATH/url.split('/')[-1]), "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return str(COMPONENT_DOWNLOAD_PATH/url.split('/')[-1])