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
import pathlib
import traceback
import os

from digitalpy.core.serialization.serialization_facade import Serialization
from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.zmanager.impl.integration_manager_subscriber import (
    IntegrationManagerSubscriber,
)
from digitalpy.core.zmanager.impl.integration_manager_pusher import (
    IntegrationManagerPusher,
)
from digitalpy.core.zmanager.impl.subject_pusher import SubjectPusher
from digitalpy.core.service_management.domain.model.service_configuration import (
    ServiceConfiguration,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.digitalpy_service import (
    DigitalPyService,
    COMMAND_ACTION,
)
from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.zmanager.response import Response


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

    # The path to the blueprints directory in this module
    base_blueprints = pathlib.Path(__file__).parent / "blueprints"

    def __init__(
        self,
        service: ServiceConfiguration,
        integration_manager_subscriber: IntegrationManagerSubscriber,
        integration_manager_pusher: IntegrationManagerPusher,
        subject_pusher: SubjectPusher,
        blueprint_path: pathlib.Path,
        blueprint_import_base: str,
        serialization: Serialization,
    ):
        super().__init__(
            service_id="digitalpy.core_api",
            service=service,
            subject_pusher=subject_pusher,
            integration_manager_subscriber=integration_manager_subscriber,
            integration_manager_pusher=integration_manager_pusher,
        )
        self.blueprint_path = blueprint_path
        self.blueprint_import_base = blueprint_import_base
        self.serialization = serialization

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
            self.handle_connection(
                message
            )  # add the specific service information to the connection message

        # handle disconnection otherwise call the api message handler
        if message.get_value("action") == "disconnection":
            self.handle_disconnection(
                message.get_value("client"), message
            )  # disconnect the client

        else:
            self.handle_api_message(message)

    def response_handler(self, response: Response):
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
        self._subject_pusher.push_container(message, self.configuration.name)

    def serialize(self, message: Response):
        """This function is used to serialize a message object to a json dictionary. The message object is updated in place."""
        if message.has_value("message"):
            serialized = self.serialization.serialize_node_to_json(
                **message.get_values()
            )
            message.set_value("message", serialized)

    def handle_response(self, response: Response):
        """This function is used to handle a response message. It is intiated by the event loop."""
        self.serialize(response)
        self.protocol.send_response(response)

    def handle_exception(self, exception: Exception):
        """This function is used to handle exceptions that occur in the service.
        It is intiated by the event loop.

        Args:
            exception (Exception): the exception that occurred
        """
        if isinstance(exception, SystemExit):
            self.status = ServiceStatusEnum.STOPPED.value
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
                    self.blueprint_import_base + "." + filename.strip(".py")
                )

                # get the blueprint from the file
                blueprints.append(blueprint_module.page)
                
        # iterate through base blueprints
        for filename in os.listdir(ApiService.base_blueprints):
            if filename.endswith(".py") and filename != "__init__.py":
                blueprint_module = importlib.import_module(
                    "digitalpy.core.api.blueprints." + filename.strip(".py")
                )
                blueprints.append(blueprint_module.page)
        return blueprints

    def start(
        self,
        object_factory: DefaultFactory,
        tracing_provider: TracingProvider,  # pylint: disable=useless-super-delegation
        configuration_factory: ConfigurationFactory,
    ):
        """We override the start method to allow for the injection of the endpoints and handlers
        to the network interface.
        """
        SingletonConfigurationFactory.configure(configuration_factory)
        ObjectFactory.configure(object_factory)
        self.tracer = tracing_provider.create_tracer(self.service_id)
        self.initialize_controllers()
        self.initialize_connections()

        # get all blueprints from the configured blueprint path
        blueprints = self._get_blueprints()

        self.protocol.initialize_network(
            self.configuration.host,
            self.configuration.port,
            blueprints=blueprints,
            service_desc=self._service_conf,
        )
        self.status = ServiceStatusEnum.RUNNING.value
        self.execute_main_loop()
