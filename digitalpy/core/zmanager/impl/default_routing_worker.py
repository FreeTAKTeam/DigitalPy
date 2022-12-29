import uuid
import zmq
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
    ):
        self.configuration = configuration
        self.factory = factory
        self.action_mapper = sync_action_mapper
        self.server_address = server_address
        self.formatter = formatter
        self.worker_id = str(uuid.uuid4())

    def initiate_sockets(self):
        context = zmq.Context()
        self.sock = context.socket(zmq.REP)
        self.sock.connect(self.server_address)
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
        except Exception as e:
            pass

    def start(self):
        self.initiate_sockets()
        self.initialize_metrics()
        self.initialize_tracing()
        while True:
            try:
                print("listening")
                topic_section, response_topic, request = self.receive_request()

                response = ObjectFactory.get_new_instance("response")
                referrer = request.get_sender()
                context = request.get_context()
                action = request.get_action()
                response.set_sender(referrer)
                response.set_context(context)
                response.set_action(action)
                response.set_format(topic_section[6])

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
                    self.sock.send_multipart(
                        [
                            response_topic.encode("utf-8"),
                            "ActionKey undefined".encode("utf-8"),
                        ]
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
                    self.formatter.serialize(response)
                    print("sending on %s", response_topic)
                    self.sock.send_multipart(
                        [
                            response_topic.encode("utf-8"),
                            response.get_values(),
                        ]
                    )
                    continue
                
                self.process_next_request(controllerClass=controllerClass,response=response)

                self.formatter.serialize(response)

                self.sock.send_multipart(
                    [
                        response_topic.encode("utf-8"),
                        response.get_values(),
                    ]
                )
            except Exception as e:
                try:
                    self.sock.send_multipart(
                        [
                            response_topic.encode("utf-8"),
                            f"error thrown {str(e)}".encode("utf-8"),
                        ]
                    )
                except Exception as e:
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

    def receive_request(self):
        message = self.sock.recv_multipart()
        topic = message[0]

        print("received topic %s" % topic)

        topic_section = topic.decode("utf-8").split("/")

        request_id = topic_section[7]

        response_topic = f"/routing/response/{topic_section[3]}/{topic_section[4]}/{topic_section[5]}/{topic_section[6]}/{request_id}"

        request = ObjectFactory.get_new_instance("request")
        request.values = message[1]
        request.set_sender(topic_section[3])
        request.set_context(topic_section[4])
        request.set_action(topic_section[5])
        request.set_format(topic_section[6])

        self.formatter.deserialize(request)
        return topic_section,response_topic,request
