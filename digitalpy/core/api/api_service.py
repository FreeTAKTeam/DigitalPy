"""
This module defines the ApiService class, a subclass of the DigitalPyService class, which is 
designed to manage API services in a digitalpy environment.

The ApiService class initializes with several parameters used to configure the service and 
establish http network communication. It contains a main event loop for the service, initiated 
by the service manager.

The module imports necessary modules and types from various components of the `digitalpy` package,
including `NetworkClient`, `ObjectFactory`, `Formatter`, `DigitalPyService`, `ServiceStatus`,
`NetworkSyncInterface`, `Request`, `DefaultFactory`, `TracingProvider`, `Response`, and 
`ServiceDescription`.

The `CONFIGURATION_SECTION` constant is also defined in this module, which is used to specify the configuration section for the core API in the digitalpy environment.
"""

import importlib
import os
import pathlib
import time
import traceback
from typing import List
from digitalpy.core.domain.domain.network_client import NetworkClient

from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.service_management.digitalpy_service import DigitalPyService, COMMAND_ACTION
from digitalpy.core.service_management.domain.service_status import ServiceStatus
from digitalpy.core.network.network_sync_interface import NetworkSyncInterface
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.zmanager.response import Response
from digitalpy.core.service_management.domain.service_description import ServiceDescription

CONFIGURATION_SECTION = "digitalpy.core_api"


class ApiService(DigitalPyService):
    """
    The ApiService class is a subclass of the DigitalPyService class and is designed to manage 
    API services in a digitalpy environment.

    This class initializes with several parameters including service_id, subject_address, 
    subject_port, subject_protocol, integration_manager_address, integration_manager_port, 
    integration_manager_protocol, formatter, network, protocol, service_desc, blueprint_path, 
    and blueprint_import_base. These parameters are used to configure the service and establish 
    network communication.

    The `event_loop` method is the main event loop for the ApiService. It is initiated by the 
    service manager.

    The `blueprint_path` and `blueprint_import_base` attributes are used to manage the blueprint
    for the service which are used to handle requests by the networks and define the output
    contexts and actions.
    """
    def __init__(self, service_id: str, subject_address: str, subject_port: int,  # pylint: disable=useless-super-delegation
                 subject_protocol: str, integration_manager_address: str,
                 integration_manager_port: int, integration_manager_protocol: str,
                 formatter: Formatter, network: NetworkSyncInterface, protocol: str,
                 service_desc: ServiceDescription, blueprint_path, blueprint_import_base: str):
        super().__init__(
            service_id, subject_address, subject_port, subject_protocol,
            integration_manager_address, integration_manager_port, integration_manager_protocol,
            formatter, network, protocol, service_desc)
        self.blueprint_path = blueprint_path
        self.blueprint_import_base = blueprint_import_base

    def handle_connection(self, client: NetworkClient, req: Request):
        """This function is used to handle client connections. It is initiated by the event loop.

        Args:
            client (NetworkClient): the client that is connecting
            req (Request): the request message

        Returns:
            None
        """
        super().handle_connection(client, req)
        req.set_context("api")
        req.set_format("pickled")
        req.set_value("source_format", self.protocol)
        req.set_action("authenticate")
        client: 'NetworkClient' = req.get_value("client")
        client.protocol = self.protocol
        client.service_id = self.service_id
        req.set_value("user_id", str(client.get_oid()))
        self.subject_send_request(req, self.protocol)

    def handle_inbound_message(self, message: Request):
        """This function is used to handle inbound messages from other services. 
        It is intiated by the event loop.

        Args:
            message (Request): the request message

        Returns:
            None
        """

        # TODO: discuss this with giu and see if we should move the to the action mapping system?
        if message.get_value("action") == "connection":
            self.handle_connection(message.get_value("client"), message)

        elif message.get_value("action") == "disconnection":
            self.handle_disconnection(message.get_value("client"), message)

        else:
            self.handle_api_message(message)

    def response_handler(self, responses: List[Response]):
        for response in responses:
            if response.get_action() == COMMAND_ACTION:
                self.handle_command(response)
            else:
                self.handle_response(response)

    def handle_api_message(self, message: Request):
        """this method is responsible for handling the case where a client sends a request.
        Args:
            message (request): the request message
        """
        message.set_format("pickled")
        message.set_value("source_format", self.protocol)
        self.subject_send_request(message, self.protocol)

    def handle_response(self, response: Response):
        self.network.send_response(response)

    def handle_exception(self, exception: Exception):
        """This function is used to handle exceptions that occur in the service. 
        It is intiated by the event loop.

        Args:
            exception (Exception): the exception that occurred
        """
        if isinstance(exception, SystemExit):
            self.status = ServiceStatus.STOPPED
        else:
            traceback.print_exc()
            print("An exception occurred: " + str(exception))

    def _get_blueprints(self):
        """get all blueprints from the configured blueprint path"""
        blueprints = []

        # Iterate through each file in the directory
        for filename in os.listdir(pathlib.Path(self.blueprint_path).absolute()):
            # Check if the file is a python file
            if filename.endswith(".py") and filename != "__init__.py":

                # import the file
                blueprint_module = importlib.import_module(
                    self.blueprint_import_base+"."+filename.strip(".py"))

                # get the blueprint from the file
                blueprints.append(blueprint_module.page)
        return blueprints

    def start(self, object_factory: DefaultFactory, tracing_provider: TracingProvider,  # pylint: disable=useless-super-delegation
              host: str = "", port: int = 0,) -> None:
        """We override the start method to allow for the injection of the endpoints and handlers
        to the network interface.
        """
        ObjectFactory.configure(object_factory)
        self.tracer = tracing_provider.create_tracer(self.service_id)
        self.initialize_controllers()
        self.initialize_connections(self.protocol)

        # get all blueprints from the configured blueprint path
        blueprints = self._get_blueprints()

        self.network.intialize_network(
            host, port, blueprints=blueprints, service_desc=self.service_desc)
        self.status = ServiceStatus.RUNNING
        self.execute_main_loop()
