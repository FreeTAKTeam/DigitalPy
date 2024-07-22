"""
This module is responsible for modifying the component filesystem.
"""

import io
import os
import shutil
import zipfile
from pathlib import PurePath
from tempfile import TemporaryFile
from typing import TYPE_CHECKING, Generator

from digitalpy.core.component_management.configuration.component_management_constants import (
    COMPONENT_DOWNLOAD_PATH, ID, RELATIVE_MANIFEST_PATH)
from digitalpy.core.component_management.controllers.component_manifest_controller import \
    ComponentManifestController
from digitalpy.core.component_management.domain.builder.component_builder_impl import \
    ComponentBuilderImpl
# import builders
from digitalpy.core.component_management.domain.builder.error_builder import \
    ErrorBuilder
from digitalpy.core.component_management.domain.model.component import \
    Component
from digitalpy.core.main.controller import Controller

from .component_management_persistence_controller_impl import \
    Component_managementPersistenceControllerImpl

if TYPE_CHECKING:
    from digitalpy.core.component_management.domain.model.error import Error
    from digitalpy.core.component_management.impl.default_facade import \
        DefaultFacade
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.domain.domain.network_client import NetworkClient
    from digitalpy.core.zmanager.impl.default_action_mapper import \
        DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response


class ComponentFilesystemController(Controller):
    """This class is responsible for managing the physical components in the file system."""

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

        if configuration:
            self.component_installation_path: str = configuration.get_section(
                "ComponentManagement"
            ).get("component_installation_path", None)

            self.component_blueprint_path: str = configuration.get_section(
                "ComponentManagement"
            ).get("component_blueprint_path", None)

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller.
        It is intiated by the service manager."""
        return super().initialize(request, response)

    def unzip_component(self, component: Component) -> dict:
        """this method is used to unzip a component and add its blueprint to the blueprint
        directory, it returns the component manifest as a dictionary and sets the commponent 
        installation path.

        Args:
            component (Component): the component to unzip

        Raises:
            ValueError: if the manifest UUID does not match the given component UUID

        Returns:
            dict: the component manifest
        """
        with zipfile.ZipFile(
            COMPONENT_DOWNLOAD_PATH / f"{component.name}.zip", "r"
        ) as zip_ref:
            with io.TextIOWrapper(
                zip_ref.open(RELATIVE_MANIFEST_PATH), encoding="utf-8"
            ) as stream:
                manifest = self.component_manifest_controller.read_manifest(stream)
                if component.UUID and manifest[ID] != component.UUID:
                    raise ValueError(
                        "The manifest UUID does not match the given component UUID"
                    )

            zip_ref.extractall(
                self._get_component_path(component),
            )

        # move the blueprint to the blueprint directory
        os.rename(
            PurePath(
                self.component_installation_path,
                component.name,
                component.name + "_blueprint.py",
            ),
            self._get_blueprint_path(component),
        )
        component.installationPath = str(self._get_component_path(component))
        return manifest

    def search_component_directory(
        self,
    ) -> Generator[tuple[PurePath, PurePath], None, None]:
        """this method is used to search the component directory potential components

        Args:
            path (str): the path to search

        Returns:
            list: a list of tuples containing the potential component oath and its facade path
        """
        potential_components = os.scandir(self.component_installation_path)
        for potential_component in potential_components:
            facade_path = PurePath(
                potential_component.path, potential_component.name + "_facade.py"
            )
            if os.path.exists(facade_path):
                yield PurePath(potential_component), facade_path

    def delete_component(self, component: Component):
        """this method is used to delete a component from the file system

        Args:
            component (Component): the component to delete
        """
        shutil.rmtree(self._get_component_path(component))

        # remove the blueprint from the blueprint directory
        os.remove(self._get_blueprint_path(component))

    def restore_files(self, temp_files: dict[PurePath, io.FileIO]):
        """this method is used to restore a set of files to their original location

        Args:
            component (Component): the component to restore the files of
        """
        for file, temp_file in temp_files.items():
            with open(file, "wb") as f:
                f.write(temp_file.read())
                temp_file.close()

    def copy_temp_files(
        self, persistent_files: list[PurePath]
    ) -> dict[PurePath, io.FileIO]:
        """this method is used to save the persistent files of a component to a temporary file
        and returns a dictionary mapping their original path to the temporary file for restoration.

        Args:
            component (Component): the component to delete the files of

        Returns:
            dict: a dictionary mapping the original path of the file to the temporary file
        """
        temp_files = {}
        for file in persistent_files:
            temp_file = TemporaryFile()
            with open(file, "rb") as f:
                temp_file.write(f.read())
            temp_files[file] = temp_file
        return temp_files

    def find_persistent_files(self, component: Component) -> list[PurePath]:
        """this method is used to save the persistent files of a component

        Args:
            component (Component): the component to save the persistent files of

        Returns:
            list: a list of the persistent files
        """
        # get all db files, currently these are the only persistent files, this will be expanded
        # to include other configuration files in the future
        db_files = []
        for root, _, files in os.walk(component.installationPath):
            for file in files:
                if file.endswith(".db"):
                    db_files.append(PurePath(root, file))
        return db_files

    def _get_blueprint_path(self, component: Component) -> "PurePath":
        """this method is used to get the blueprint path of a component

        Args:
            component (Component): the component to get the blueprint path of

        Returns:
            PurePath: the blueprint path
        """
        return PurePath(self.component_blueprint_path, component.name + "_blueprint.py")

    def _get_component_path(self, component: Component) -> "PurePath":
        """this method is used to get the component path of a component

        Args:
            component (Component): the component to get the component path of

        Returns:
            PurePath: the component path
        """
        if component.installationPath is not None and component.installationPath != "None":
            return PurePath(component.installationPath)
        else:
            return PurePath(self.component_installation_path, component.name)

    def get_external_action_mapping_path(self, component: Component) -> "PurePath":
        """this method is used to get the external action mapping path of a component

        Args:
            component (Component): the component to get the external action mapping path of

        Returns:
            PurePath: the external action mapping path
        """
        return PurePath(
            self._get_component_path(component)
            / "configuration/external_action_mapping.ini"
        )
