from typing import List, Tuple
import uuid
import zmq
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.digipy_configuration.action_key import ActionKey
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.persistence.application_event import ApplicationEvent
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.impl.config_action_key_provider import ConfigActionKeyProvider
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.main.factory import Factory
from digitalpy.core.telemetry.impl.opentel_metrics_provider import OpenTelMetricsProvider


class DefaultRoutingWorker:
    def __init__(
        self,
        factory: Factory,
        configuration: Configuration,
        sync_action_mapper: ActionMapper,
        formatter: Formatter,
        server_address: str,
        integration_manager_address: str
    ):
        self.configuration = configuration
        self.factory = factory
        self.action_mapper = sync_action_mapper
        self.server_address = server_address
        self.integration_manager_address = integration_manager_address
        self.formatter = formatter
        self.worker_id = str(uuid.uuid4())

    def initiate_sockets(self):
        context = zmq.Context()
        self.sock = context.socket(zmq.PULL)
        self.sock.connect(self.server_address)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.sock.setsockopt(zmq.RCVHWM, 0)
        self.integration_manager_sock = context.socket(zmq.PUSH)
        self.integration_manager_sock.connect(self.integration_manager_address)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.integration_manager_sock.setsockopt(zmq.SNDHWM, 0)
        self.action_mapper = self.action_mapper
        ObjectFactory.configure(self.factory)

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
        try:
            self.tracing_provider = self.factory.get_instance("tracingprovider")
            self.factory.register_instance(
                "tracingproviderinstance", self.tracing_provider
            )
        except Exception as ex:
            raise ex

    def send_response(self, response: Response, protocol):
        self.formatter.serialize(response)
        message = protocol.encode()+b","+response.get_values()
        self.integration_manager_sock.send(message)

    def send_error(self, exception: Exception):
        self.integration_manager_sock.send(b"error,"+str(exception).encode("utf-8"))
    
    def start(self):
        self.initiate_sockets()
        self.initialize_metrics()
        self.initialize_tracing()
        while True:
            try:
                print("listening")
                response_topic, request = self.receive_request()

                response = ObjectFactory.get_new_instance("response")
                referrer = request.get_sender()
                context = request.get_context()
                action = request.get_action()
                format = request.get_format()
                response.set_sender(referrer)
                response.set_context(context)
                response.set_action(action)
                response.set_format(format)

                actionKeyProvider = ConfigActionKeyProvider(
                    self.configuration, "actionmapping"
                )

                actionKey = ActionKey.get_best_match(
                    actionKeyProvider,
                    request.get_sender(),
                    request.get_context(),
                    request.get_action(),
                )

                if len(actionKey) == 0:
                    # return, if action key is not defined
                    self.send_error(
                        Exception(f"action key for action {request.get_action()} undefined")
                    )
                    continue

                # get next controller
                controllerClass = None
                controllerDef = self.configuration.get_value(actionKey, "actionmapping")
                if len(controllerDef) == 0:
                    self.logger.error(
                        "No controller found for best action key "
                        + actionKey
                        + ". Request was referrer?context?action"
                    )
                    Exception(request, response)

                # check if the controller definition contains a method besides the class name
                controllerMethod = None
                if "." in controllerDef:
                    controller_def_list = controllerDef.split(".")
                    controllerClass = ".".join(controller_def_list[:-1])
                    controllerMethod = controller_def_list[-1]
                else:
                    controllerClass = controllerDef

                # instantiate controller
                controllerObj = ObjectFactory.get_instance_of(
                    controllerClass,
                )

                # everything is right in place, start processing

                # self.formatter.deserialize(request)

                # initialize controller
                controllerObj.initialize(request, response)

                # execute controller
                try:
                    print("executing %s", action)
                    controllerObj.execute(controllerMethod)
                    print("%s executed", action)
                except Exception as e:
                    pass
                # check if an action key exists for the return action
                nextActionKey = ActionKey.get_best_match(
                    actionKeyProvider,
                    controllerClass,
                    response.get_context(),
                    response.get_action(),
                )

                # terminate
                # - if there is no next action key or
                # - if the next action key is the same as the previous one (to prevent recursion)
                terminate = len(nextActionKey) == 0 or actionKey == nextActionKey
                if terminate:
                    # stop processing
                    print("sending on %s", response_topic)
                    self.send_response(response, response_topic)
                    continue
                
                self.process_next_request(controllerClass=controllerClass,response=response)

                self.formatter.serialize(response)

                self.send_response(response, protocol=response_topic)
            except Exception as ex:
                try:
                    self.send_error(ex)
                except Exception as e:
                    self.send_error(ex)
                    print(str(e))

    def process_next_request(self, controllerClass, response):
        # set the request based on the result
        nextRequest = ObjectFactory.get_new_instance("request")
        nextRequest.set_sender(controllerClass)
        nextRequest.set_context(response.get_context())
        nextRequest.set_action(response.get_action())
        nextRequest.set_format(response.get_format())
        nextRequest.set_values(response.get_values())
        # nextRequest.set_errors(response.get_errors())
        # nextRequest.set_response_format(request.get_response_format())
        self.action_mapper.process_action(nextRequest, response)

    def receive_request(self) -> Tuple[str, Request]:
        """Receive and process a request from the ZMQ socket.

        Returns:
            A tuple containing the topic sections as a list, the response topic as a string, and the request object.
        """
        try:
            # Receive message from client
            message = self.sock.recv_multipart()[0]            
            sender, context, action, format, protocol, values = message.split(b",", 5)
            # Construct the response topic

            # Create a new request object
            request = ObjectFactory.get_new_instance("request")
            request.values = values
            request.set_sender(sender.decode("utf-8"))
            request.set_context(context.decode("utf-8"))
            request.set_action(action.decode("utf-8"))
            request.set_format(format.decode("utf-8"))

            # Deserialize the request
            self.formatter.deserialize(request)

            response_topic = f'/{protocol.decode()}/{request.get_value("service_id")}/{sender.decode("utf-8")}/{context.decode("utf-8")}/{action.decode("utf-8")}'

            # Return the topic sections, response topic, and request
            return response_topic, request
        except Exception as ex:
            self.send_error(ex)