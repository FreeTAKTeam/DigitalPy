"""
This is the main controller class of the application. Every operation of the controller is realized by this file
OOTB. It is recommended that you (the developper) avoid adding further methods to the file and instead add supporting
controllers with these methods should you need them. This controller is called directly by the facade in order to
fulfil any requests made to the component by default.
"""

from typing import TYPE_CHECKING, List

from digitalpy.core.main.controller import Controller
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
# import builders
from digitalpy.core.component_management.domain.builder.component_builder import ComponentBuilder
from digitalpy.core.component_management.domain.builder.error_builder import ErrorBuilder
from .component_management_persistence_controller import Component_ManagementPersistenceController

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient
    from digitalpy.core.component_management.domain.model.component import Component
    from digitalpy.core.component_management.domain.model.error import Error

class Component_ManagementController(Controller):

    def __init__(self, request: 'Request',
                 response: 'Response',
                 sync_action_mapper: 'DefaultActionMapper',
                 configuration: 'Configuration'):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.Component_builder = ComponentBuilder(request, response, sync_action_mapper, configuration)
        self.Error_builder = ErrorBuilder(request, response, sync_action_mapper, configuration)
        self.Component_Management_persistence_controller = Component_ManagementPersistenceController(
            request, response, sync_action_mapper, configuration)

    def initialize(self, request: 'Request', response: 'Response'):
        """This function is used to initialize the controller. 
        It is intiated by the service manager."""
        self.Component_builder.initialize(request, response)
        self.Error_builder.initialize(request, response)
        self.Component_Management_persistence_controller.initialize(request, response)
        return super().initialize(request, response)
    def DELETEComponent(self, ID: str, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """TODO"""
        db_records = self.Component_Management_persistence_controller.get_component(ID = ID)
        domain_records: List['Component'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Component_builder.build_empty_object(config_loader=config_loader)
            self.Component_builder.add_object_data(record)
            record = self.Component_builder.get_result()
            self.Component_Management_persistence_controller.remove_component(record)
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def POSTComponent(self, body: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """TODO"""

        # initialize Component builder
        self.Component_builder.build_empty_object(config_loader=config_loader)
        self.Component_builder.add_object_data(mapped_object = body, protocol=Protocols.JSON)
        domain_obj = self.Component_builder.get_result()

        # Save the Component record to the database
        self.Component_Management_persistence_controller.save_component(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def GETComponent(self, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """TODO"""
        # retrieve the Component record from the database
        db_records = self.Component_Management_persistence_controller.get_all_component()
        domain_records: List['Component'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Component_builder.build_empty_object(config_loader=config_loader)
            self.Component_builder.add_object_data(record)
            domain_records.append(self.Component_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def PATCHComponent(self, body: 'Component',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """TODO"""
        # create the basic domain object from the json data
        self.Component_builder.build_empty_object(config_loader)
        self.Component_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Component_builder.get_result()

        # get from the database
        db_obj = self.Component_Management_persistence_controller.get_component(oid=str(domain_obj.oid))[0]

        # initialize the object
        self.Component_builder.build_empty_object(config_loader)
        self.Component_builder.add_object_data(db_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        self.Component_builder.add_object_data(body, Protocols.JSON)
        # Save the Schedule record to the database
        self.Component_Management_persistence_controller.update_component(domain_obj)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

        # publish the records
        self.response.set_action("publish")

    def GETComponentId(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """TODO"""

        # retrieve the Component record from the database
        db_records = self.Component_Management_persistence_controller.get_component(ID = ID)
        domain_records: List['Component'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Component_builder.build_empty_object(config_loader=config_loader)
            self.Component_builder.add_object_data(record)
            domain_records.append(self.Component_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

        # publish the records
        self.response.set_action("publish")

    def POSTInstallAllComponents(self, Directory: 'str', import_root: 'str', client: 'NetworkClient', config_loader, *args, **kwargs): # pylint: disable=unused-argument
        """install all components that are not installed yet"""
        return None

    def GETComponentStatus(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs): # pylint: disable=unused-argument
        """returns the status of the component or the last error"""
        return None

    def POSTComponentRegister(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs) -> 'Component' : # pylint: disable=unused-argument
        """register a component"""
        return None

    def GETComponentDiscovery(self, Directory: 'str', import_root: 'str', client: 'NetworkClient', config_loader, *args, **kwargs) -> 'Component' : # pylint: disable=unused-argument
        """discover a list of components, other than list components, returns also components that are not activated or installed"""
        return None

