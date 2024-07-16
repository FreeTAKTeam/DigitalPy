"""
This module is responsible for discovering components and all the operations that are related to this task.
"""

import io
from typing import TYPE_CHECKING, Generator
from pathlib import PurePath

import os
import importlib
import zipfile

from digitalpy.core.component_management.configuration.component_management_constants import (
    COMPONENT_DOWNLOAD_PATH,
    RELATIVE_MANIFEST_PATH,
    ID,
)

from digitalpy.core.component_management.controllers.component_manifest_controller import (
    ComponentManifestController,
)
from digitalpy.core.component_management.domain.builder.component_builder_impl import (
    ComponentBuilderImpl,
)
from digitalpy.core.main.object_factory import ObjectFactory


from digitalpy.core.main.controller import Controller

# import builders
from digitalpy.core.component_management.domain.builder.component_builder import (
    ComponentBuilder,
)
from digitalpy.core.component_management.domain.builder.error_builder import (
    ErrorBuilder,
)
from .component_management_persistence_controller import (
    Component_ManagementPersistenceController,
)
from digitalpy.core.component_management.domain.model.component import Component

if TYPE_CHECKING:
    from digitalpy.core.component_management.impl.default_facade import DefaultFacade
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient

    from digitalpy.core.component_management.domain.model.error import Error


class ComponentInstallationController(Controller):
    """In accordance with the SRP this controller is responsible for discovering components
    and all the operations that are related to this task.
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
        self.Error_builder = ErrorBuilder(
            request, response, sync_action_mapper, configuration
        )
        self.Component_Management_persistence_controller = (
            Component_ManagementPersistenceController(
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

            self.component_import_root: str = configuration.get_section(
                "ComponentManagement"
            ).get("component_import_root", None)

            self.component_blueprint_path: str = configuration.get_section(
                "ComponentManagement"
            ).get("component_blueprint_path", None)

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller.
        It is intiated by the service manager."""
        self.Component_builder.initialize(request, response)
        self.Error_builder.initialize(request, response)
        self.Component_Management_persistence_controller.initialize(request, response)
        return super().initialize(request, response)

    def install_component(self, component: Component, config_loader) -> Component:
        """this method is used to install a component

        Args:
            component_path (str): the path to the component

        Returns:
            Component: the installed component
        """

        with zipfile.ZipFile(
            COMPONENT_DOWNLOAD_PATH / f"{component.name}.zip", "r"
        ) as zip_ref:
            if component.UUID:
                with io.TextIOWrapper(
                    zip_ref.open(RELATIVE_MANIFEST_PATH), encoding="utf-8"
                ) as stream:
                    manifest = self.component_manifest_controller.read_manifest(stream)
                    if not manifest[ID] == component.UUID:
                        raise ValueError(
                            "The manifest UUID does not match the given component UUID"
                        )

            zip_ref.extractall(
                PurePath(self.component_installation_path, component.name)
            )

            # move the blueprint to the blueprint directory
            os.rename(
                PurePath(
                    self.component_installation_path,
                    component.name,
                    component.name + "_blueprint.py",
                ),
                PurePath(
                    self.component_blueprint_path, component.name + "_blueprint.py"
                ),
            )
            component = self._register_component(
                PurePath(self.component_installation_path, component.name),
                manifest,
                config_loader,
            )
            return component

    def register_all_components(self, config_loader) -> list[Component]:
        """this method is used to install all components in the component installation directory

        Args:
            config_loader: the configuration loader to use
        """
        components: list[Component] = []

        # get all potential components in the directory
        for (
            potential_component,
            facade_path,
        ) in self.search_component_directory(self.component_installation_path):
            # retrieve the manifest
            with open(
                facade_path.parent / RELATIVE_MANIFEST_PATH, "r", encoding="utf-8"
            ) as stream:
                manifest = self.component_manifest_controller.read_manifest(stream)

            # validate the manifest
            if not self.component_manifest_controller.validate_manifest(
                manifest=manifest, component_name=potential_component.name
            ):
                continue

            # install the component
            component = self._register_component(
                potential_component, manifest, config_loader
            )

            components.append(component)

        return components

    def _register_component(
        self,
        potential_component: "PurePath",
        manifest: "dict",
        config_loader,
    ) -> "Component":
        """this method is used to install a component

        Args:
            potential_component (PurePath): the component to install
            manifest (dict): the manifest of the component
            config_loader: the configuration loader to use

        Returns:
            Component: the installed component
        """
        config = ObjectFactory.get_instance("Configuration")
        facade = self.retrieve_facade(potential_component)
        # create the component object and add it to the list
        self.Component_builder.build_empty_object(config_loader=config_loader)
        self.Component_builder.add_object_data(manifest)
        component_obj = self.Component_builder.get_result()

        facade.register(config)
        # get the component from the database if it exists or save to the db
        db_components = self.Component_Management_persistence_controller.get_component(
            UUID=component_obj.UUID
        )
        if len(db_components) > 0:
            db_component = db_components[0]
        else:
            db_component = (
                self.Component_Management_persistence_controller.save_component(
                    component_obj
                )
            )

        self.Component_builder.build_empty_object(config_loader=config_loader)
        self.Component_builder.add_object_data(db_component)
        return self.Component_builder.get_result()

    def search_component_directory(
        self, path: "str"
    ) -> Generator[tuple[PurePath, PurePath], None, None]:
        """this method is used to search the component directory potential components

        Args:
            path (str): the path to search

        Returns:
            list: a list of components found in the directory
        """
        potential_components = os.scandir(path)
        for potential_component in potential_components:
            facade_path = PurePath(
                potential_component.path, potential_component.name + "_facade.py"
            )
            if os.path.exists(facade_path):
                yield PurePath(potential_component), facade_path

    def retrieve_facade(self, component_path: "PurePath") -> "DefaultFacade":
        """this method is used to validate a component

        Args:
            component_path (str): the component to validate

        Returns:
            DefaultFacade: the component facade
        """
        component_name = component_path.name.replace("_component", "")

        component_facade = getattr(
            importlib.import_module(
                f"{self.component_import_root}.{component_path.name}.{component_name}_facade"
            ),
            f"{''.join([name.capitalize() if name[0].isupper()==False else name for name in component_name.split('_')])}",
        )

        facade_instance: "DefaultFacade" = component_facade(
            ObjectFactory.get_instance("SyncActionMapper"),
            ObjectFactory.get_new_instance("request"),
            ObjectFactory.get_new_instance("response"),
            ObjectFactory.get_instance("configuration"),
        )

        return facade_instance
