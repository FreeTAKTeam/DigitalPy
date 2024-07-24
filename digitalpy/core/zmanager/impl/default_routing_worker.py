import logging
import multiprocessing
import threading
import uuid
from typing import List, Tuple

import zmq

from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.factory import Factory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.service_management.digitalpy_service import COMMAND_PROTOCOL
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER,
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
        configuration: Configuration,
        sync_action_mapper: ActionMapper,
        formatter: Formatter,
        subject_address: str,
        integration_manager_address: str,
        integration_manager_pub_address: int,
        timeout: int = 2000,
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
            subject_address (str): the subject_address to receive requests from
            integration_manager_address (str): the integration_manager address to send responses to
            integration_manager_pub_address (int): the integration_manager pub address to subscribe to
            timeout (int, optional): the timeout for the sockets. Defaults to 2000.
        """
        self.configuration = configuration
        self.factory = factory
        self.action_mapper = sync_action_mapper
        self.subject_address = subject_address
        self.integration_manager_address = integration_manager_address
        self.integration_manager_pub_address = integration_manager_pub_address
        self.formatter = formatter
        self.worker_id = str(uuid.uuid4())
        self.logger = logging.getLogger("DP-Default_Routing_Worker_DEBUG")
        self.logger.setLevel(logging.DEBUG)

        self.context: zmq.Context = None
        self.sub_sock: zmq.Socket = None
        self.integration_manager_sock: zmq.Socket = None
        self.subject_sock: zmq.Socket = None

        self.timeout: int = timeout

        self.running = multiprocessing.Event()
        self.running.set()

    def initiate_sockets(self):
        """initiate all socket connections"""
        self.context = zmq.Context()
        self._create_subject_listener_sock()

        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self._create_integration_manager_pusher_sock()

        # TODO: determine the correct topic to subscribe to
        self._create_integration_manager_sub_sock()

        self.action_mapper = self.action_mapper
        ObjectFactory.configure(self.factory)

    def _create_integration_manager_sub_sock(self):
        self.sub_sock = self.context.socket(zmq.SUB)
        self.sub_sock.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.sub_sock.setsockopt_string(zmq.SUBSCRIBE, "/messagesrouting_worker")
        self.sub_sock.connect(self.integration_manager_pub_address)
        self.sub_sock.setsockopt(zmq.LINGER, 0)

    def _create_integration_manager_pusher_sock(self):
        self.integration_manager_sock = self.context.socket(zmq.PUSH)
        self.integration_manager_sock.connect(self.integration_manager_address)

        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.integration_manager_sock.setsockopt(zmq.SNDHWM, 0)
        self.integration_manager_sock.setsockopt(zmq.LINGER, 0)
        self.integration_manager_sock.setsockopt(zmq.SNDTIMEO, self.timeout)

    def _create_subject_listener_sock(self):
        self.subject_sock = self.context.socket(zmq.PULL)
        self.subject_sock.connect(self.subject_address)
        self.subject_sock.setsockopt(zmq.RCVHWM, 0)
        self.subject_sock.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.subject_sock.setsockopt(zmq.LINGER, 0)

    def teardown(self):
        """teardown the environment"""
        self.running.clear()
        self.sub_sock.close()
        self.integration_manager_sock.close()
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

    def send_response(self, response: Response, protocol: str, service_id: str) -> None:
        """send a response to the integration_manager

        Args:
            response (Response): the response to be sent to integration_manager
            protocol (str): the protocol of the message
        """
        response_topics = self.get_response_topic(response, protocol, service_id)
        self.logger.debug(
            "sending response \n id: %s \n values: %s \n topics: %s",
            str(response.get_id()),
            str(response.get_values()),
            str(response_topics),
        )
        # self.formatter.serialize(response)
        # response_value = response.get_values()
        for response_topic in response_topics:
            self.integration_manager_sock.send(response_topic)

    def send_error(self, exception: Exception):
        """send an exception to the integration_manager

        Args:
            exception (Exception): the exception to be sent to the integration_manager
        """
        self.integration_manager_sock.send(b"error," + str(exception).encode("utf-8"))

    def start(self):
        """start the routing worker"""
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
        """listen for requests from the subject, process them, and send responses back to the integration_manager"""
        while self.running.is_set():
            try:
                protocol, request = self.receive_request()
                service_id = request.get_value("service_id")
                # if the protocol is COMMAND_PROTOCOL, then the request is a command to a service and should
                # be sent directly to integration_manager so that it can be processed by the service
                if protocol == COMMAND_PROTOCOL:
                    self.send_response(
                        request, protocol, request.get_value("service_id")
                    )

                else:
                    response = self.process_request(protocol, request)
                    self.send_response(
                        response, protocol=protocol, service_id=service_id
                    )
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
                self.process_integration_manager_message(message.split(b" ")[1:])
            except zmq.error.Again:
                pass
            except Exception as ex:
                self.logger.error(ex)
                self.send_error(ex)

    def process_integration_manager_message(self, message: list[bytes]):
        """process a message published by the integration manager

        Args:
            request (Request): the request to be processed
        """
        # TODO: add business logic to process the message
        print(message)

    def process_request(self, protocol: str, request: Request):
        """process a request made by the subject

        Args:
            response_topic (str): the base topic from which to send the response
            request (Request): the request object to be processed
        """
        response: Response = ObjectFactory.get_new_instance("response")
        referrer = request.get_sender()
        context = request.get_context()
        action = request.get_action()
        format = request.get_format()
        response.set_sender(referrer)
        response.set_context(context)
        response.set_action(action)
        response.set_format(format)
        response.set_id(request.get_id())

        self.action_mapper.process_action(request, response)
        self.logger.debug("returned values: %s", str(response.get_values()))
        return response

    def get_response_topic(
        self, response: Response, protocol: str, service_id: str
    ) -> List[bytes]:
        """get the topic to which the response is to be sent

        Args:
            response (Response): the response to be sent to the
                integration manager which may or may not have a value
                of topics

            protocol (str): the protocol on which the message is sent

            service_id (str): the service to which the message is sent

        Return:
            List[bytes]
        """
        if isinstance(response.get_value("topics"), list):
            return response.get_value("topics")
        else:
            message = f"/{service_id}/{protocol}/{response.get_sender()}/{response.get_context()}/{response.get_action()}/{response.get_id()}/".encode()
            self.formatter.serialize(response)
            response_value = response.get_values()
            return [message + ZMANAGER_MESSAGE_DELIMITER + response_value]

    def process_next_request(self, controller_class: str, response: Response):
        """process the next request based on the response from the previous request

        Args:
            controllerClass (str): this is the controller class name from which the response originated
            response (Response): the response to be processed as the next request
        """
        # set the request based on the result
        next_request = ObjectFactory.get_new_instance("request")
        next_request.set_sender(controller_class)
        next_request.set_context(response.get_context())
        next_request.set_action(response.get_action())
        next_request.set_format(response.get_format())
        next_request.set_values(response.get_values())
        # nextRequest.set_errors(response.get_errors())
        # nextRequest.set_response_format(request.get_response_format())
        self.action_mapper.process_action(next_request, response)

    def receive_request(self) -> Tuple[str, Request]:
        """Receive and process a request from the ZMQ socket.

        Returns:
            A tuple containing the topic sections as a list, the response topic as a string, and the request object.
        """
        try:
            # Receive message from client
            message = self.subject_sock.recv_multipart().pop(0)
            sender, context, action, format, protocol, id, values = message.split(
                ZMANAGER_MESSAGE_DELIMITER, 6
            )

            # Create a new request object
            request = ObjectFactory.get_new_instance("request")
            request.values = values
            request.set_sender(sender.decode("utf-8"))
            request.set_context(context.decode("utf-8"))
            request.set_action(action.decode("utf-8"))
            request.set_format(format.decode("utf-8"))
            request.set_id(id.decode("utf-8"))

            # Deserialize the request
            self.formatter.deserialize(request)

            self.logger.debug(
                "received request \n sender: %s \n context: %s \n action: %s \n format: %s \n protocol: %s \n id: %s \n values: %s",
                str(sender),
                str(context),
                str(action),
                format,
                protocol,
                id,
                request.get_values(),
            )
            # Return the topic sections, response topic, and request
            return protocol.decode(), request

        except Exception as ex:
            self.send_error(ex)
