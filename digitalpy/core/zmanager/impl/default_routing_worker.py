import logging
import multiprocessing
import threading
import uuid

import zmq

from digitalpy.core.zmanager.impl.integration_manager_pusher import (
    IntegrationManagerPusher,
)
from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)
from digitalpy.core.serialization.controllers.serializer_action_key import (
    SerializerActionKey,
)
from digitalpy.core.zmanager.domain.model.zmanager_configuration import (
    ZManagerConfiguration,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.main.factory import Factory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.service_management.digitalpy_service import COMMAND_PROTOCOL
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER,
)
from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    MAX_FLOW_LENGTH,
)

from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response


class DefaultRoutingWorker:
    """this class is the default routing worker for the ZManager. It can be thought of as a sandbox for
    the Digitalpy components to run within. It receives requests from the subject, processes them, and sends
    responses back to the integration_manager."""

    def __init__(
        self,
        factory: Factory,
        sync_action_mapper: ActionMapper,
        formatter: Formatter,
        integration_manager_pusher: IntegrationManagerPusher,
    ):
        """this is the default constructor for the DefaultRoutingWorker class

        Args:
            factory (Factory): this is the factory which will be used by the ObjectFactory singleton
                to instantiate objects.
            configuration (Configuration): a configuration object with an index of all action
                mapping routes.
            sync_action_mapper (ActionMapper): the synchronous action mapper used to actually route
                requests.
            formatter (Formatter): the formatter used to serialize requests and responses to and
                from their value.
        """
        self.factory = factory
        self.action_mapper = sync_action_mapper
        self.subject_address = SingletonConfigurationFactory.get_configuration_object(
            "ZManagerConfiguration"
        ).subject_push_address
        self.formatter = formatter
        self.worker_id = str(uuid.uuid4())
        self.logger = logging.getLogger("DP-Default_Routing_Worker_DEBUG")
        self.logger.setLevel(logging.DEBUG)
        self.integration_manager_pusher = integration_manager_pusher

        self.zmanager_configuration: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )

        self.serializer_action_key: SerializerActionKey = ObjectFactory.get_instance(
            "SerializerActionKey"
        )
        self.serializer_container: SerializerContainer = ObjectFactory.get_instance(
            "SerializerContainer"
        )
        self.action_key_controller: ActionKeyController = ObjectFactory.get_instance(
            "ActionKeyController"
        )
        self.action_flow_controller: ActionFlowController = ObjectFactory.get_instance(
            "ActionFlowController"
        )

        self.context: zmq.Context = None
        self.sub_sock: zmq.Socket = None
        self.integration_manager_sock: zmq.Socket = None
        self.subject_sock: zmq.Socket = None

        self.running = multiprocessing.Event()
        self.running.set()

    def initiate_sockets(self):
        """initiate all socket connections"""
        self.context = zmq.Context()
        self._create_subject_listener_sock()

        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.integration_manager_pusher.setup()

        # TODO: determine the correct topic to subscribe to
        self._create_integration_manager_sub_sock()

        self.action_mapper = self.action_mapper
        ObjectFactory.configure(self.factory)

    def _create_integration_manager_sub_sock(self):
        self.sub_sock = self.context.socket(zmq.SUB)
        self.sub_sock.setsockopt(
            zmq.RCVTIMEO, self.zmanager_configuration.worker_timeout
        )
        ak = self.action_key_controller.new_action_key()
        # TODO: determine the correct decorator and config to subscribe to
        ak.decorator = "ROUTING_WORKER"
        ak.config = "UPDATE_ROUTING_WORKERS"
        topic = self.serializer_action_key.to_generic_topic(ak)
        self.sub_sock.setsockopt(zmq.SUBSCRIBE, topic)
        self.sub_sock.connect(
            self.zmanager_configuration.integration_manager_pub_address
        )

        # do not wait for messages to be sent to the socket before terminating the context,
        self.sub_sock.setsockopt(zmq.LINGER, 0)

    def _create_subject_listener_sock(self):
        self.subject_sock = self.context.socket(zmq.PULL)
        self.subject_sock.connect(self.subject_address)
        self.subject_sock.setsockopt(zmq.RCVHWM, 0)
        self.subject_sock.setsockopt(
            zmq.RCVTIMEO, self.zmanager_configuration.worker_timeout
        )
        self.subject_sock.setsockopt(zmq.LINGER, 0)

    def teardown(self):
        """teardown the environment"""
        self.running.clear()
        self.sub_sock.close()
        self.integration_manager_pusher.teardown()
        self.subject_sock.close()
        # self.context.term()

    def initialize_metrics(self):
        """initialize the metrics provider and register it to the factory
        so it can be used by all called components"""
        try:
            self.metrics_provider = self.factory.get_instance(
                "metricsprovider",
                dynamic_configuration={"service_name": self.worker_id},
            )
            self.factory.register_instance(
                "metrics_provider_instance", self.metrics_provider
            )
        except Exception as e:
            pass

    def initialize_tracing(self):
        """initialize tracing system

        Raises:
            ex: raises thrown exceptions
        """
        try:
            self.tracing_provider = self.factory.get_instance("tracingprovider")
            self.factory.register_instance(
                "tracingproviderinstance", self.tracing_provider
            )
        except Exception as ex:
            raise ex

    def send_error(self, exception: Exception):
        """send an exception to the integration_manager

        Args:
            exception (Exception): the exception to be sent to the integration_manager
        """
        self.integration_manager_sock.send(
            b"new error," + str(exception).encode("utf-8")
        )

    def start(self, factory: Factory, configuration_factory: ConfigurationFactory):
        """start the routing worker"""
        ObjectFactory.configure(factory)
        SingletonConfigurationFactory.configure(configuration_factory)
        self.initiate_sockets()
        self.initialize_metrics()
        self.initialize_tracing()

        subject_thread = threading.Thread(target=self._subject_listener)

        integration_manager_thread = threading.Thread(
            target=self._integration_manager_listener
        )

        subject_thread.start()
        integration_manager_thread.start()

        subject_thread.join()
        integration_manager_thread.join()

        self.teardown()

        return

    def _subject_listener(self):
        """listen for requests from the subject, process them, and send responses
        back to the integration_manager"""
        while self.running.is_set():
            try:
                request = self.receive_request()
                response = self.process_request(request)
                self.integration_manager_pusher.push_container(response)
            except zmq.error.Again:
                pass
            except Exception as ex:
                try:
                    self.send_error(ex)
                except Exception as ex:
                    self.send_error(ex)
                    logging.error(ex)

    def _integration_manager_listener(self):
        """listen for messages from the integration_manager and process them"""
        while self.running.is_set():
            try:
                message = self.sub_sock.recv_multipart().pop()
                self.logger.debug("received message %s", str(message))
                self.process_integration_manager_message(message)
            except zmq.error.Again:
                pass
            except Exception as ex:
                self.logger.error(ex)
                self.send_error(ex)

    def process_integration_manager_message(self, message: list[bytes]):
        """process a message published by the integration manager, this is a placeholder
        for future functionality

        Args:
            request (Request): the request to be processed
        """
        # TODO: add business logic to process the message
        print(message)

    def process_request(self, request: Request):
        """process a request made by the subject until the default routing worker cannot resolve
        the action_key to a specific action at which point the method exits. Alternatively
        if the number of actions processed exceeds the MAX_FLOW_LENGTH the method will exit.

        Args:
            response_topic (str): the base topic from which to send the response
            request (Request): the request object to be processed
        """
        response: Response = ObjectFactory.get_new_instance("response")
        response.action_key = request.action_key
        response.set_id(request.get_id())

        # alternative to while loop
        for _ in range(MAX_FLOW_LENGTH):
            # get the next action in the flow before any changes are made to the request object
            next_action = self.action_flow_controller.get_next_message_action(request)
            # execute the current action
            self.action_mapper.process_action(request, response)
            # if there is a next action that we can resolve, set it as the action key
            # this assumes the Publish action is reserved to signify that the response
            # should be sent to the integration manager
            response.action_key = next_action
            if self.action_flow_controller.is_end_of_flow(next_action):
                break
            try:
                # ensure that the next action is a valid action key and resolve it
                next_action = self.action_key_controller.resolve_action_key(next_action)
                # set the next action
                request.action_key = next_action
                # set the request to the previous response
                request.set_values(response.get_values())
            # if the next action is not a valid action key, break the loop
            except ValueError:
                break
        self.logger.debug("returned values: %s", str(response.get_values()))
        return response

    def receive_request(self) -> Request:
        """Receive and process a request from the ZMQ socket.

        Returns:
            Request: the request object to be processed
        """
        # Receive message from client
        message = self.subject_sock.recv_multipart().pop(0)
        return self.serializer_container.from_zmanager_message(message)
