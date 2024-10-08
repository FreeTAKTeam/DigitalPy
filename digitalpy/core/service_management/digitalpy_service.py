"""
This file defines a class `DigitalPyService`

The class constructor takes several parameters including service id, addresses, ports, protocols, 
a formatter, and a network interface. It initializes the parent classes and sets up various 
properties.

The class has several properties with their respective getters and setters, such as 
`protocol`, `status`, and `tracer`.

The class also defines several methods, some of which are abstract and must be implemented 
by any class that inherits from `DigitalPyService`. These include `event_loop`, 
`handle_command`, and `handle_exception`.

The `start` method is used to start the service. It configures the object factory, 
initializes the tracer, initializes the controllers, and starts the event loop. 
If a network is provided, it also initializes the network.

The `__getstate__` and `__setstate__` methods are used for pickling and unpickling the object, 
respectively.
"""

#######################################################
#
# DigitalPyService.py
# Python implementation of the Class DigitalPyService
# Generated by Enterprise Architect
# Created on:      02-Dec-2022 5:39:44 PM
# Original author: Giu Platania
#
#######################################################
from abc import abstractmethod
from datetime import datetime
from multiprocessing import Process
import traceback
from typing import List, Optional

from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.zmanager.impl.subject_pusher import SubjectPusher
from digitalpy.core.zmanager.impl.integration_manager_subscriber import (
    IntegrationManagerSubscriber,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.service_management.domain.model.service_configuration import (
    ServiceConfiguration,
)
from digitalpy.core.zmanager.domain.model.zmanager_configuration import (
    ZManagerConfiguration,
)
from digitalpy.core.domain.domain.service_health import ServiceHealth
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.domain.model.service_operations import (
    ServiceOperations,
)

from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.telemetry.tracer import Tracer
from digitalpy.core.network.network_interface import NetworkInterface
from digitalpy.core.zmanager.response import Response
from digitalpy.core.IAM.IAM_facade import IAM
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.zmanager.request import Request
from digitalpy.core.health.domain.service_health_category import ServiceHealthCategory
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration

COMMAND_PROTOCOL = "command"
COMMAND_ACTION = "ServiceCommand"


class DigitalPyService:
    """
    Represents a DigitalPy service.

    This class is responsible for managing the lifecycle and behavior of a DigitalPy service.
    It inherits from the Service.

    Args:
        service_id (str): The unique ID of the service inheriting from DigitalPyService.
        formatter (Formatter): The formatter used by the service to serialize the request
            values to and from messages.
        service_conf (Service): The configuration of the service.
        error_threshold (float, optional): The error threshold for the service. Defaults to 0.1.
    """

    # TODO: there must be a better solution than passing the service description as a parameter but for now
    # it's necessary to be shared with the network so that the network can initialize the network clients
    # with the service information

    def __init__(
        self,
        service_id: str,
        service: ServiceConfiguration,
        integration_manager_subscriber: IntegrationManagerSubscriber,
        subject_pusher: SubjectPusher,
        error_threshold: float = 0.1,
    ):
        """the constructor for the digitalpy service class

        Args:
            service_id (str): the unique id of the service
            formatter (Formatter): the formatter used by the service to serialize the request values to and from messages, (should be injected by object factory)
            protocol (NetworkInterface): the network interface used by the service to send and receive messages, (should be injected by object factory through the services' constructor)
        """
        self._integration_manager_subscriber = integration_manager_subscriber
        self._subject_pusher = subject_pusher
        self._service_conf = service
        self._zmanager_configuration: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )
        self.subject_address = self._zmanager_configuration.subject_pull_address
        self.integration_manager_address = (
            self._zmanager_configuration.integration_manager_pub_address
        )
        self.service_id = service_id
        self._tracer = None
        self.protocol: NetworkInterface = ObjectFactory.get_instance(
            self.configuration.protocol
        )
        self.response_queue: List[Response] = []
        self.iam_facade: IAM = ObjectFactory.get_instance("IAM")
        self.total_requests = 0
        self.total_errors = 0
        self.total_request_processing_time = 0
        self.error_threshold = error_threshold
        self._process: Optional[Process] = None

    def handle_connection(self, message: Request):
        """register a client with the server. This method should be called when a client connects to the server
        so that it can be registered with the IAM component.
        Args:
            message (Request): the request from the client containing connection data
        """
        client: NetworkClient = message.get_value("client")
        client.service_id = self.service_id
        client.protocol = self.configuration.protocol
        resp = ObjectFactory.get_new_instance("Response")
        message.set_value("connection", client)
        self.iam_facade.initialize(message, resp)
        self.iam_facade.execute("connection")
        return message

    def handle_disconnection(self, client: NetworkClient, req: Request):
        """unregister a client from the server. This method should be called when a client disconnects from the server
        so that it can be unregistered from the IAM component.
        Args:
            client (NetworkClient): the client to unregister
            req (Request): the request from the client containing disconnection data
        """
        resp = ObjectFactory.get_new_instance("Response")
        req.set_value("connection_id", str(client.get_oid()))
        self.iam_facade.initialize(req, resp)
        self.iam_facade.execute("disconnection")
        return

    @property
    def process(self) -> Process:
        """get the process of the service

        Returns:
            Process: the process of the service
        """
        return self._process

    @process.setter
    def process(self, value: Process):
        """set the process of the service

        Args:
            value (Process): the process of the service
        """
        self._process = value

    @property
    def configuration(self) -> ServiceConfiguration:
        """get the configuration of the service

        Returns:
            Configuration: the configuration of the service
        """
        return self._service_conf

    @configuration.setter
    def configuration(self, value: ServiceConfiguration):
        """set the configuration of the service

        Args:
            value (Service): the configuration of the service
        """
        self._service_conf = value

    @property
    def status(self) -> str:
        """get the status of the service

        Returns:
            ServiceStatus: the status of the service
        """
        return self._service_conf.status

    @status.setter
    def status(self, status: str):
        self._service_conf.status = status

    @property
    def tracer(self) -> Tracer:
        """get the tracer of the service

        Raises:
            ValueError: if the tracer has not been initialized it will raise a value error

        Returns:
            Tracer: the tracer of the service
        """
        if self._tracer is None:
            raise ValueError("Tracer has not been initialized")
        else:
            return self._tracer

    @tracer.setter
    def tracer(self, value: Tracer):
        """set the tracer of the service

        Args:
            value (Tracer): the tracer of the service

        Raises:
            ValueError: if the tracer has already been initialized it will raise a value error
            ValueError: if the value is not an instance of Tracer it will raise a value error
        """
        if self._tracer is not None:
            raise ValueError("Tracer has already been initialized")
        elif not isinstance(value, Tracer):
            raise ValueError("Tracer must be an instance of TracingProvider")
        self._tracer = value

    @abstractmethod
    def serialize(self, message: Request) -> bytes:
        """used to serialize a message to bytes. Should be overriden by inheriting classes"""

    def discovery(self):
        """used to  inform the discoverer of the specifics of this service"""
        # TODO: the contract for discovery needs to be established
        # example for potential implementation
        return "service desc"

    def send_heart_beat(self):
        """used to inform the service menager that this service is still alive"""
        # TODO: once the service manager has been well defined then we will need
        # to define the format for this service.

    def initialize_controllers(self):
        """used to initialize the controllers once the service is started. Should be overriden
        by inheriting classes
        """

    def initialize_connections(self):
        """initialize connections to the subject and the integration manager within the
        zmanager architecture.
        """
        self._integration_manager_subscriber.setup()
        self._subject_pusher.setup()

    def response_handler(self, response: Response):
        """used to handle a response. Should be overriden by inheriting classes"""
        if response.get_action() == COMMAND_ACTION:
            self.handle_command(response)
        else:
            self.handle_response(response)

    def handle_response(self, response: Response):
        """used to handle a response. Should be overriden by inheriting classes"""
        if self.protocol:
            response.set_value("client", response.get_value("recipients"))
            self.serialize(response)
            self.protocol.send_response(response)

    def event_loop(self):
        """used to run the service. Should be overriden by inheriting classes"""
        if self.protocol:
            self.handle_network()

        response = (
            self._integration_manager_subscriber.fetch_integration_manager_response()
        )
        if response:
            self.response_handler(response)

    def handle_network(self):
        """used to handle the network."""
        requests = self.protocol.service_connections()
        for request in requests:
            self.handle_inbound_message(request)

    def stop(self):
        """
        Stops the service by performing necessary cleanup operations.

        This method sets the service status to STOPPING, tears down the network if it exists,
        disconnects the broker, tears down connections, sets the service status to STOPPED,
        and raises SystemExit to exit the program.
        """
        self.status = ServiceStatusEnum.STOPPING.value

        if self.protocol:
            self.protocol.teardown_network()

        self._integration_manager_subscriber.teardown()
        self._subject_pusher.teardown()

        self.status = ServiceStatusEnum.STOPPED.value

        raise SystemExit

    def handle_inbound_message(self, message: Request) -> bool:
        """This function is used to handle inbound messages from other services.
        It is intiated by the event loop.

        Args:
            message (Request): the message to handle

        Returns:
            bool: True if the message was handled successfully, False otherwise
        """
        # TODO: discuss this with giu and see if we should move the to the action mapping system?
        if message.get_value("action") == "connection":
            self.handle_connection(message)
            return True

        elif message.get_value("action") == "disconnection":
            self.handle_disconnection(message.get_value("client"), message)
            return True

        return False

    def _subscribe_to_commands(self):
        """used to subscribe to commands"""
        command_action: ActionKey = ActionKey(None, None)
        command_action.action = COMMAND_ACTION
        command_action.config = self.service_id
        self._integration_manager_subscriber.subscribe_to_action(command_action)

    def _subscribe_to_flows(self):
        """used to subscribe to flows"""
        for flow_id in self.configuration.flows:
            flow = SingletonConfigurationFactory.get_action_flow(flow_id)
            flow_done_action: ActionKey = ActionKey(None, None)
            flow_done_action.config = flow
            flow_done_action.action = "done"
            self._integration_manager_subscriber.subscribe_to_action(flow_done_action)

    def handle_command(self, command: Response):
        """used to handle a command. Should be overriden by inheriting classes"""
        if command.get_value("command") == ServiceOperations.STOP.value:
            self.stop()
        elif command.get_value("command") == ServiceOperations.GET_HEALTH.value:
            service_health = self.get_health()
            conf: Configuration = ObjectFactory.get_instance("Configuration")
            resp = ObjectFactory.get_new_instance("Response")
            resp.set_value("message", service_health)
            resp.set_action("publish")
            resp.set_format("pickled")
            resp.set_id(command.get_id())
            self._subject_pusher.push_container(
                resp, conf.get_value("service_id", "ServiceManager")
            )

    def get_health(self):
        """used to get the health of the service."""
        service_health: ServiceHealth = ServiceHealth()
        if self.total_requests == 0:
            service_health.error_percentage = 0
            service_health.average_request_time = 0
        else:
            service_health.error_percentage = self.total_errors / self.total_requests
            service_health.average_request_time = (
                self.total_request_processing_time / self.total_requests
            )
        service_health.service_id = self.service_id
        service_health.status = self.calculate_health(service_health)
        service_health.timestamp = datetime.now()
        return service_health

    def calculate_health(self, service_health: ServiceHealth):
        """used to calculate the health of the service."""
        if service_health.error_percentage > self.error_threshold:
            return ServiceHealthCategory.DEGRADED
        else:
            return ServiceHealthCategory.OPERATIONAL

    def handle_exception(self, exception: Exception):
        """This function is used to handle exceptions that occur in the service.
        It is intiated by the event loop.
        """
        if isinstance(exception, SystemExit):
            self.status = ServiceStatusEnum.STOPPED.value
            raise SystemExit
        else:
            traceback.print_exc()
            print("An exception occurred: " + str(exception))
            self.total_errors += 1

    def start(
        self,
        object_factory: DefaultFactory,
        tracing_provider: TracingProvider,
        conf_factory: ConfigurationFactory,
    ):
        """used to start the service and initialize the network if provided

        Args:
            object_factory (DefaultFactory): the object factory used to create instances of objects
            tracing_provider (TracingProvider): the tracing provider used to create a tracer
        """
        SingletonConfigurationFactory.configure(conf_factory)
        ObjectFactory.configure(object_factory)
        self.tracer = tracing_provider.create_tracer(self.service_id)
        self.initialize_controllers()
        self.initialize_connections()

        self.protocol.initialize_network(
            self.configuration.host,
            self.configuration.port,
            service_desc=self._service_conf,
        )

        self.status = ServiceStatusEnum.RUNNING.value
        self.execute_main_loop()

    def execute_main_loop(self):
        """used to execute the main loop of the service"""
        while self.status == ServiceStatusEnum.RUNNING.value:
            try:
                self.event_loop()
            except Exception as ex:
                self.handle_exception(ex)
        if self.status == ServiceStatusEnum.STOPPED.value:
            exit(0)
