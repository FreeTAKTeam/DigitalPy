from typing import TYPE_CHECKING


from digitalpy.core.component_management.controllers.component_discovery_controller import ComponentDiscoveryController
from digitalpy.core.component_management.controllers.component_installation_controller import (
    ComponentInstallationController,
)
from digitalpy.core.component_management.controllers.component_management_controller import (
    Component_ManagementController,
)
from digitalpy.core.main.object_factory import ObjectFactory

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

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient
    from digitalpy.core.component_management.domain.model.component import Component
    from digitalpy.core.component_management.domain.model.error import Error


class Component_ManagementControllerImpl(Component_ManagementController):

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
        self.component_installation_controller = ComponentInstallationController(
            request, response, sync_action_mapper, configuration
        )
        self.component_discovery_controller = ComponentDiscoveryController(
            request, response, sync_action_mapper, configuration
        )

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller.
        It is intiated by the service manager."""
        self.Component_builder.initialize(request, response)
        self.Error_builder.initialize(request, response)
        self.Component_Management_persistence_controller.initialize(request, response)
        self.component_installation_controller.initialize(request, response)
        self.component_discovery_controller.initialize(request, response)
        return super().initialize(request, response)

    def GETComponentStatus(
        self, ID: str, client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """returns the status of the component or the last error"""
        return None

    def POSTComponentRegister(
        self, ID: str, client: "NetworkClient", config_loader, *args, **kwargs
    ) -> "Component":  # pylint: disable=unused-argument
        """register a component"""
        components = self.Component_Management_persistence_controller.get_component(
            UUID=ID
        )
        if len(components) <= 0:
            return None
        component = components[0]

        # instantiate the facade
        facade = self.component_installation_controller.retrieve_facade(
            component.installation_path, component.import_root
        )

        # register the configuration
        facade.register(ObjectFactory.get_instance("Configuration"))

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [component])

        # publish the records
        self.response.set_action("publish")

    def POSTInstallAllComponents(
        self,
        Directory: "str",
        import_root: "str",
        config_loader,
        *args,
        **kwargs,
    ):  # pylint: disable=unused-argument
        """this method is used to discover zipped components in a given directory

        Args:
            component_folder_path (str): the path in which to search for components. the searchable
            folder should be in the following format:\n
                component_folder_path \n
                |-- component_A.zip
                |-- component_B.zip
        Returns:
            List[str]: a list of available components in the given path
        """
        self.component_installation_controller.install_all_components(
            Directory, import_root, config_loader
        )

        # return the records
        # self.response.set_value("message", components)

        # publish the records
        self.response.set_action("publish")

    def GETComponentDiscovery(
        self,
        Directory: "str",
        import_root: "str",
        client: "NetworkClient",
        config_loader,
        *args,
        **kwargs,
    ) -> "Component":  # pylint: disable=unused-argument
        """discover a list of components, other than list components, returns also components that are not activated or installed"""
        components: list["Component"] = []
        for component in self.component_discovery_controller.discover_components(Directory, config_loader):
            components.append(component)

        self.response.set_action("publish")
        self.response.set_value("message", components)