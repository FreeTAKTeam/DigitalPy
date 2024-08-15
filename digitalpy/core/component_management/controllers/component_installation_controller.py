"""
This module is responsible for discovering components and all the operations that are related to 
this task.
"""

import importlib
import os
from typing import TYPE_CHECKING

from digitalpy.core.files.files_facade import Files
from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.digipy_configuration.impl.inifile_configuration import (
    InifileConfiguration,
)
from digitalpy.core.component_management.domain.model.component_management_configuration import (
    ComponentManagementConfiguration,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.component_management.configuration.component_management_constants import (
    RELATIVE_MANIFEST_PATH,
)
from digitalpy.core.component_management.controllers.component_filesystem_controller import (
    ComponentFilesystemController,
)
from digitalpy.core.component_management.controllers.component_manifest_controller import (
    ComponentManifestController,
)
from digitalpy.core.component_management.domain.builder.component_builder_impl import (
    ComponentBuilderImpl,
)

# import builders
from digitalpy.core.component_management.domain.builder.error_builder import (
    ErrorBuilder,
)
from digitalpy.core.component_management.domain.model.component import Component
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory

from .component_management_persistence_controller_impl import (
    Component_managementPersistenceControllerImpl,
)

if TYPE_CHECKING:
    from digitalpy.core.component_management.domain.model.error import Error
    from digitalpy.core.component_management.impl.default_facade import DefaultFacade
    from digitalpy.core.digipy_configuration.domain.model.configuration import (
        Configuration,
    )
    from digitalpy.core.domain.domain.network_client import NetworkClient
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response


class ComponentInstallationController(Controller):
    """This class is responsible for discovering components and all the operations that
    are related to managing the components in the file system. It is responsible for installing,
    uninstalling, updating, and registering components.
    """

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

        self.component_filesystem_controller = ComponentFilesystemController(
            request, response, sync_action_mapper, configuration
        )

        self.component_management_configuration: ComponentManagementConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ComponentManagementConfiguration"
            )
        )

        self.action_flow_controller: ActionFlowController = ObjectFactory.get_instance(
            "ActionFlowController"
        )

        self.files: Files = ObjectFactory.get_instance("files")

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller.
        It is intiated by the service manager."""
        self.component_builder.initialize(request, response)
        self.error_builder.initialize(request, response)
        self.component_management_persistence_controller.initialize(request, response)
        self.component_filesystem_controller.initialize(request, response)
        return super().initialize(request, response)

    def install_component(self, component: Component) -> dict:
        """this method is used to install a component

        Args:
            component (Component): the initial component to install

        Raises:
            ValueError: if the manifest is invalid

        Returns:
            dict: the component manifest
        """

        component_manifest = self.component_filesystem_controller.unzip_component(
            component
        )

        # validate the manifest
        if not self.component_manifest_controller.validate_manifest(
            manifest=component_manifest, component_name=component.name
        ):
            # delete the component if the manifest is invalid
            self.component_filesystem_controller.delete_component(component)
            raise ValueError("Manifest validation failed")

        # get the component object
        self.register_component(component)

        return component_manifest

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
        ) in self.component_filesystem_controller.search_component_directory():
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

            # get component object
            component = self._get_component(manifest, config_loader)

            # register the component
            self.register_component(component)

            component.installationPath = str(potential_component)

            component.isActive = True

            component.isInstalled = True

            # add the component to the list
            components.append(component)

        return components

    def register_component(
        self,
        component: "Component",
    ):
        """this method is used to register a component in the central configuration

        Args:
            component (Component): the component to register
        """

        # create the component object and add it to the list

        facade: DefaultFacade = self.retrieve_facade(component)

        ObjectFactory.register_instance(
            f"{component.name.lower()}actionmapper",
            facade.get_action_mapper(),
        )

        component_configuration = InifileConfiguration(facade.get_configuration_path())
        component_configuration.add_configuration("")
        SingletonConfigurationFactory.add_configuration(component_configuration)

        flow_path = facade.get_flow_configuration_path()
        if flow_path:
            flow_file = self.files.get_file(flow_path)
            self.action_flow_controller.create_action_flow(flow_file)

        facade.setup()

    def _get_component(self, manifest, config_loader):
        """this method is used to get a component object from a manifest

        Args:
            manifest: the manifest to use
            config_loader: the configuration loader to use
        """
        self.component_builder.build_empty_object(config_loader=config_loader)
        self.component_builder.add_object_data(manifest)
        component_obj = self.component_builder.get_result()
        return component_obj

    def retrieve_facade(self, component: "Component") -> "DefaultFacade":
        """this method is used to validate a component

        Args:
            component (Component): the component to validate

        Returns:
            DefaultFacade: the component facade
        """

        component_facade = getattr(
            importlib.import_module(
                f"{self.component_management_configuration.component_import_root}.{component.name}.{component.name}_facade"
            ),
            f"{''.join([name.capitalize() if name[0].isupper() is False else name for name in component.name.split('_')])}",
        )

        facade_instance: "DefaultFacade" = component_facade(
            ObjectFactory.get_instance("SyncActionMapper"),
            ObjectFactory.get_new_instance("request"),
            ObjectFactory.get_new_instance("response"),
            ObjectFactory.get_instance("configuration"),
        )

        return facade_instance

    def uninstall_component(self, component: Component):
        """this method is used to uninstall a component

        Args:
            component (Component): the component to uninstall
        """

        external_action_mapping = (
            self.component_filesystem_controller.get_external_action_mapping_path(
                component
            )
        )

        if not os.path.exists(external_action_mapping):
            raise FileNotFoundError(
                f"External action mapping not found at {external_action_mapping}"
            )

        SingletonConfigurationFactory.remove_configuration(str(external_action_mapping))

        self.component_filesystem_controller.delete_component(component)

    def update_component(self, component: Component):
        """this method is used to update a component

        Args:
            component (Component): the component to update
        """

        # identify files that are persistent
        persistent_files = self.component_filesystem_controller.find_persistent_files(
            component
        )

        # save the persistent files
        temp_files = self.component_filesystem_controller.copy_temp_files(
            persistent_files
        )

        # uninstall the component
        self.uninstall_component(component)

        # install the new component
        self.install_component(component)

        # restore the persistent files
        self.component_filesystem_controller.restore_files(temp_files)
