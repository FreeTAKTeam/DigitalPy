from pathlib import PurePath
from typing import TYPE_CHECKING, Union

from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.component_management.controllers.component_discovery_controller import (
    ComponentDiscoveryController,
)
from digitalpy.core.component_management.controllers.component_installation_controller import (
    ComponentInstallationController,
)
from digitalpy.core.component_management.controllers.component_management_controller import (
    Component_ManagementController,
)
from digitalpy.core.component_management.controllers.component_pull_controller import (
    ComponentPullController,
)
from digitalpy.core.domain.domain.network_client import NetworkClient
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
        self.component_pull_controller = ComponentPullController(
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

    def POSTComponent(
        self, body: str, client: NetworkClient, config_loader, *args, **kwargs
    ):
        """install a component which has been discovered. This endpoint assumes that the component
        has been discovered and is ready to be installed, it also assumes that the component is
        in the current discovery directory.

        """
        # initialize Component builder
        self.Component_builder.build_empty_object(config_loader=config_loader)
        self.Component_builder.add_object_data(
            mapped_object=body, protocol=Protocols.JSON
        )
        component = self.Component_builder.get_result()

        # install the component
        self.component_installation_controller.install_component(
            component
        )

        # return the records
        self.response.set_value("message", [component])

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # publish the records
        self.response.set_action("publish")

    def POSTComponentRegister(
        self, ID: str, client: "NetworkClient", config_loader, *args, **kwargs
    ) -> "Component":  # pylint: disable=unused-argument
        """register a component"""
        components = self.Component_Management_persistence_controller.get_component(
            UUID=ID
        )
        self.component_installation_controller.register_component(components[0])

    def POSTInstallAllComponents(
        self,
        config_loader,
        client: Union["NetworkClient", None] = None,
        *args,
        **kwargs,
    ):  # pylint: disable=unused-argument
        """this method is used to discover zipped components in a given directory.

        Returns:
            List[str]: a list of available components in the given path
        """
        components = self.component_installation_controller.register_all_components(
            config_loader
        )

        for component in components:
            existing_components = self.Component_Management_persistence_controller.get_component(UUID=component.UUID)
            if len(existing_components) > 0:
                self.Component_Management_persistence_controller.update_component(component)
            else:
                self.Component_Management_persistence_controller.save_component(component)

        # return the records
        self.response.set_value("message", components)

        # publish the records
        self.response.set_action("publish")

        # allow calling without a defined client
        if client is not None:
            # set the target
            self.response.set_value("recipients", [str(client.get_oid())])

    def GETComponentDiscovery(
        self,
        client: "NetworkClient",
        config_loader,
        *args,
        **kwargs,
    ) -> list["Component"]:  # pylint: disable=unused-argument
        """discover a list of components, other than list components, returns also components
        that are not activated or installed"""
        components: list["Component"] = []

        for component in self.component_discovery_controller.discover_components(
            config_loader
        ):
            components.append(component)

        self.response.set_action("publish")
        self.response.set_value("message", components)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])
        return components

    def PullComponent(
        self, url: str, client: "NetworkClient", config_loader, *args, **kwargs
    ) -> "PurePath":
        """pull a component from a remote datasource"""
        save_location = self.component_pull_controller.pull_component_http(
            url, config_loader
        )

        self.response.set_action("publish")
        self.response.set_value("message", [save_location])
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])
        return save_location

    def DELETEComponent(
        self, ID: "str", client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""
        db_records = self.Component_Management_persistence_controller.get_component(
            oid=ID
        )

        if len(db_records) <= 0:
            raise ValueError("No record found for the given ID")
        else:
            db_record = db_records[0]

        self.Component_builder.build_empty_object(config_loader=config_loader)
        self.Component_builder.add_object_data(db_record)
        record = self.Component_builder.get_result()

        self.component_installation_controller.uninstall_component(record)

        self.Component_Management_persistence_controller.remove_component(record)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [record])

        # publish the records
        self.response.set_action("publish")

    def PATCHComponent(self, body: 'Component',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """update a component record in the database and update the component in the installation directory if necessary.
        Notably, we don't want to delete the database record.

        Args:
            body (Component): the component object to be updated
            client (NetworkClient): the client object
            config_loader (Configuration): the configuration loader
        
        Raises:
            ValueError: if the component is not found in the database
        
        Returns:
            None: return a none
        """
        # create the basic domain object from the json data
        self.Component_builder.build_empty_object(config_loader)
        self.Component_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Component_builder.get_result()

        # get from the database
        db_obj = self.Component_Management_persistence_controller.get_component(oid=str(domain_obj.oid))[0]

        if db_obj is None:
            raise ValueError("Component not found in the database")
        
        # initialize the object
        self.Component_builder.build_empty_object(config_loader)
        self.Component_builder.add_object_data(db_obj)
        # update the object with json data
        self.Component_builder.add_object_data(body, Protocols.JSON)
        
        self.component_installation_controller.update_component(self.Component_builder.get_result(), config_loader)

        # Save the Schedule record to the database
        self.Component_Management_persistence_controller.update_component(domain_obj)
        
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

        # publish the records
        self.response.set_action("publish")