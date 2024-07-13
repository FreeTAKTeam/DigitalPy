"""
This module is responsible for discovering components and all the operations that are related to this task.
"""

from typing import TYPE_CHECKING, Generator
from pathlib import PurePath

import os
import importlib

from digitalpy.core.component_management.configuration.component_management_constants import (
    MANIFEST_PATH,
    MANIFEST,
    RELATIVE_MANIFEST_PATH,
)

from digitalpy.core.component_management.controllers.component_manifest_controller import ComponentManifestController
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
        self.component_manifest_controller = ComponentManifestController(
            request, response, sync_action_mapper, configuration
        )

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller.
        It is intiated by the service manager."""
        self.Component_builder.initialize(request, response)
        self.Error_builder.initialize(request, response)
        self.Component_Management_persistence_controller.initialize(request, response)
        return super().initialize(request, response)

    def install_all_components(self, Directory: str, import_root: str, config_loader) -> None:
        """this method is used to install all components in a given path

        Args:
            Directory (str): the directory to search for components
            import_root (str): the root path to import the components from
        """
        config = ObjectFactory.get_instance("Configuration")

        # get all potential components in the directory
        for (
            potential_component,
            facade_path,
        ) in self.search_component_directory(Directory):
            # retrieve the manifest
            manifest = self.component_manifest_controller.read_manifest(
                facade_path.parent / RELATIVE_MANIFEST_PATH
            )
            # validate the manifest
            if self.component_manifest_controller.validate_manifest(
                manifest=manifest, component_name=potential_component.name
            ):
                facade = self.retrieve_facade(potential_component, import_root)
                # create the component object and add it to the list
                component_obj = self.create_component_object(
                        potential_component,
                        manifest.get_section(
                            potential_component.name + MANIFEST, include_meta=True
                        ),
                        import_root,
                        config_loader,
                    )
                self.Component_Management_persistence_controller.save_component(component_obj)
                facade.register(config)

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

    def retrieve_facade(
        self, component_path: "PurePath", import_root: "str"
    ) -> "DefaultFacade":
        """this method is used to validate a component

        Args:
            component_path (str): the component to validate
            import_root (str): the root path to import the components from

        Returns:
            DefaultFacade: the component facade
        """
        component_name = component_path.name.replace("_component", "")

        component_facade = getattr(
            importlib.import_module(
                f"{import_root}.{component_path.name}.{component_name}_facade"
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
