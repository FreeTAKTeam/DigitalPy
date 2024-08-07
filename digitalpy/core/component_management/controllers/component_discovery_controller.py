"""This module contains the ComponentDiscoveryController class."""

import io
from typing import TYPE_CHECKING, Generator, Union
from pathlib import PurePath

import os
import zipfile

from digitalpy.core.component_management.controllers.component_management_persistence_controller_impl import (
    Component_managementPersistenceControllerImpl,
)
from digitalpy.core.component_management.controllers.component_manifest_controller import (
    ComponentManifestController,
)

from digitalpy.core.component_management.domain.builder.component_builder_impl import (
    ComponentBuilderImpl,
)
from digitalpy.core.main.controller import Controller

# import builders
from digitalpy.core.component_management.domain.builder.error_builder import (
    ErrorBuilder,
)
from digitalpy.core.component_management.configuration.component_management_constants import (
    COMPONENT_DOWNLOAD_PATH,
    RELATIVE_MANIFEST_PATH,
)
from digitalpy.core.files.domain.model.extensions import Extensions

from digitalpy.core.component_management.domain.model.component import Component

if TYPE_CHECKING:
    from digitalpy.core.component_management.impl.default_facade import DefaultFacade
    from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient

    from digitalpy.core.component_management.domain.model.error import Error

class ComponentDiscoveryController(Controller):
    """This controller is responsible for discovering the **compressed** components in the
    component download directory."""

    def __init__(
        self,
        request: "Request",
        response: "Response",
        sync_action_mapper: "DefaultActionMapper",
        configuration: "Configuration",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.component_builder = ComponentBuilderImpl(
            request, response, sync_action_mapper, configuration
        )
        self.error_builder = ErrorBuilder(
            request, response, sync_action_mapper, configuration
        )
        self.component_management_persistence_controller = (
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
        self.component_builder.initialize(request, response)
        self.error_builder.initialize(request, response)
        self.component_management_persistence_controller.initialize(request, response)
        return super().initialize(request, response)

    def discover_components(self, config_loader) -> Generator[Component, None, None]:
        """this functions is used to discover components in a directory, components are
        expected to be in the form of zip files. To identify a component we simply look for
        a manifest file in the zip file under the path "[rootFolder]/configuration/manifest.ini".
        We then parse the manifest file and create a component object with the data we find.
        This function returns a generator that yields a component object for each component found.
        This function only searches a single level deep in the directory and only indexes .zip files.

        Args:
            config_loader: the configuration loader object

        Returns:
            Generator[Component, None, None]: a generator that yields a component object for each component found
        """

        for root, _, files in os.walk(COMPONENT_DOWNLOAD_PATH):
            for file in files:
                if file.endswith(Extensions.ZIP):
                    component = self._discover_component(
                        PurePath(root, file), config_loader
                    )
                    if component:
                        yield component

    def _discover_component(
        self, path: PurePath, config_loader
    ) -> Union[Component, None]:
        """This function is used to discover a single component. It reads the manifest file
        from the component zip file and creates a component object with the data found in the manifest.

        Args:
            path (PurePath): the path to the component zip file
            config_loader: the configuration loader object

        Returns:
            Component: the component object created from the manifest data
        """
        if not zipfile.is_zipfile(path):
            raise ValueError("File is not a zip file")

        with zipfile.ZipFile(path, "r") as zip_ref:
            with io.TextIOWrapper(
                zip_ref.open(name=RELATIVE_MANIFEST_PATH, mode="r"), encoding="utf-8"
            ) as manifest_file:
                manifest = self.component_manifest_controller.read_manifest(
                    manifest_file
                )
                if manifest:
                    self.component_builder.build_empty_object(config_loader)
                    self.component_builder.add_object_data(manifest, path)
                    return self.component_builder.get_result()
        return None
