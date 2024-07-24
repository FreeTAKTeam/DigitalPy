"""
This is the main controller class of the application. Every operation of the controller is 
realized by this file OOTB. It is recommended that you (the developper) avoid adding further
methods to the file and instead add supporting controllers with these methods should you 
need them. This controller is called directly by the facade in order to fulfil any requests
made to the component by default.
"""

from typing import TYPE_CHECKING, List

from digitalpy.core.main.controller import Controller
from digitalpy.core.serialization.configuration.serialization_constants import Protocols

# import builders
from digitalpy.core.component_management.domain.builder.component_builder import (
    ComponentBuilder,
)
from digitalpy.core.component_management.domain.builder.actionkey_builder import (
    ActionKeyBuilder,
)
from digitalpy.core.component_management.domain.builder.error_builder import (
    ErrorBuilder,
)
from .component_management_persistence_controller_impl import (
    Component_managementPersistenceControllerImpl,
)

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient
    from digitalpy.core.component_management.domain.model.component import Component
    from digitalpy.core.component_management.domain.model.actionkey import ActionKey
    from digitalpy.core.component_management.domain.model.error import Error


class Component_managementController(Controller):
    """This class is responsible for managing the components in the system."""
    def __init__(
        self,
        request: "Request",
        response: "Response",
        sync_action_mapper: "DefaultActionMapper",
        configuration: "Configuration",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.component_builder = ComponentBuilder(
            request, response, sync_action_mapper, configuration
        )
        self.actionkey_builder = ActionKeyBuilder(
            request, response, sync_action_mapper, configuration
        )
        self.error_builder = ErrorBuilder(
            request, response, sync_action_mapper, configuration
        )
        self.component_management_persistence_controller_impl = (
            Component_managementPersistenceControllerImpl(
                request, response, sync_action_mapper, configuration
            )
        )

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller.
        It is intiated by the service manager."""
        self.component_builder.initialize(request, response)
        self.actionkey_builder.initialize(request, response)
        self.error_builder.initialize(request, response)
        self.component_management_persistence_controller_impl.initialize(
            request, response
        )
        return super().initialize(request, response)

    def POSTComponentRequiredAlfaVersion(
        self,
        system_installedAlfaVersion: "float",
        body: "Component",
        client: "NetworkClient",
        config_loader,
        *args,
        **kwargs
    ):  # pylint: disable=unused-argument
        """"""
        return None

    def DELETEComponent(
        self, ID: str, client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""
        db_records = (
            self.component_management_persistence_controller_impl.get_component(ID=ID)
        )
        domain_records: List["Component"] = []

        # convert the records to the domain object
        for record in db_records:
            self.component_builder.build_empty_object(config_loader=config_loader)
            self.component_builder.add_object_data(record)
            record = self.component_builder.get_result()
            self.component_management_persistence_controller_impl.remove_component(
                record
            )
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def POSTComponent(
        self, body: "str", client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""

        # initialize Component builder
        self.component_builder.build_empty_object(config_loader=config_loader)
        self.component_builder.add_object_data(
            mapped_object=body, protocol=Protocols.JSON
        )
        domain_obj = self.component_builder.get_result()

        # Save the Component record to the database
        self.component_management_persistence_controller_impl.save_component(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def GETComponent(
        self, client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""
        # retrieve the Component record from the database
        db_records = (
            self.component_management_persistence_controller_impl.get_all_component()
        )
        domain_records: List["Component"] = []

        # convert the records to the domain object
        for record in db_records:
            self.component_builder.build_empty_object(config_loader=config_loader)
            self.component_builder.add_object_data(record)
            domain_records.append(self.component_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def PATCHComponent(
        self, body: "Component", client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""
        # create the basic domain object from the json data
        self.component_builder.build_empty_object(config_loader)
        self.component_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.component_builder.get_result()

        # get from the database
        db_obj = self.component_management_persistence_controller_impl.get_component(
            oid=str(domain_obj.oid)
        )[0]

        # initialize the object
        self.component_builder.build_empty_object(config_loader)
        self.component_builder.add_object_data(db_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        self.component_builder.add_object_data(body, Protocols.JSON)
        # Save the Schedule record to the database
        self.component_management_persistence_controller_impl.update_component(
            domain_obj
        )

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

        # publish the records
        self.response.set_action("publish")

    def GETComponentId(
        self, ID: "str", client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""

        # retrieve the Component record from the database
        db_records = (
            self.component_management_persistence_controller_impl.get_component(ID=ID)
        )
        domain_records: List["Component"] = []

        # convert the records to the domain object
        for record in db_records:
            self.component_builder.build_empty_object(config_loader=config_loader)
            self.component_builder.add_object_data(record)
            domain_records.append(self.component_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

        # TODO implement business logic
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", "")

        # publish the records
        self.response.set_action("publish")

    def POSTActionKey(
        self, body: "str", client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""

        # initialize Actionkey builder
        self.actionkey_builder.build_empty_object(config_loader=config_loader)
        self.actionkey_builder.add_object_data(
            mapped_object=body, protocol=Protocols.JSON
        )
        domain_obj = self.actionkey_builder.get_result()

        # Save the Actionkey record to the database
        self.component_management_persistence_controller_impl.save_actionkey(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def DELETEActionKey(
        self, ID: str, client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""
        db_records = (
            self.component_management_persistence_controller_impl.get_actionkey(ID=ID)
        )
        domain_records: List["Actionkey"] = []

        # convert the records to the domain object
        for record in db_records:
            self.actionkey_builder.build_empty_object(config_loader=config_loader)
            self.actionkey_builder.add_object_data(record)
            record = self.actionkey_builder.get_result()
            self.component_management_persistence_controller_impl.remove_actionkey(
                record
            )
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def GETActionKey(
        self, client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""
        # retrieve the Actionkey record from the database
        db_records = (
            self.component_management_persistence_controller_impl.get_all_actionkey()
        )
        domain_records: List["ActionKey"] = []

        # convert the records to the domain object
        for record in db_records:
            self.actionkey_builder.build_empty_object(config_loader=config_loader)
            self.actionkey_builder.add_object_data(record)
            domain_records.append(self.actionkey_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def PATCHActionKey(
        self, body: "ActionKey", client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""
        # create the basic domain object from the json data
        self.actionkey_builder.build_empty_object(config_loader)
        self.actionkey_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.actionkey_builder.get_result()

        # get from the database
        db_obj = self.component_management_persistence_controller_impl.get_actionkey(
            oid=str(domain_obj.oid)
        )[0]

        # initialize the object
        self.actionkey_builder.build_empty_object(config_loader)
        self.actionkey_builder.add_object_data(db_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        self.actionkey_builder.add_object_data(body, Protocols.JSON)
        # Save the Schedule record to the database
        self.component_management_persistence_controller_impl.update_actionkey(
            domain_obj
        )

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

        # publish the records
        self.response.set_action("publish")

    def GETComponentRegister(
        self, ID: "str", client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """register a component"""

        # retrieve the Component record from the database
        db_records = (
            self.component_management_persistence_controller_impl.get_component(ID=ID)
        )
        domain_records: List["Component"] = []

        # convert the records to the domain object
        for record in db_records:
            self.component_builder.build_empty_object(config_loader=config_loader)
            self.component_builder.add_object_data(record)
            domain_records.append(self.component_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def GETComponentDiscovery(
        self, client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""
        # retrieve the Component record from the database
        db_records = (
            self.component_management_persistence_controller_impl.get_all_component()
        )
        domain_records: List["Component"] = []

        # convert the records to the domain object
        for record in db_records:
            self.component_builder.build_empty_object(config_loader=config_loader)
            self.component_builder.add_object_data(record)
            domain_records.append(self.component_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def GETActionKeyId(
        self, ID: "str", client: "NetworkClient", config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """TODO"""

        # retrieve the Actionkey record from the database
        db_records = (
            self.component_management_persistence_controller_impl.get_actionkey(ID=ID)
        )
        domain_records: List["ActionKey"] = []

        # convert the records to the domain object
        for record in db_records:
            self.actionkey_builder.build_empty_object(config_loader=config_loader)
            self.actionkey_builder.add_object_data(record)
            domain_records.append(self.actionkey_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")
