import time
from digitalpy.config.action_key import ActionKey
from digitalpy.model.application_event import ApplicationEvent
from digitalpy.config.impl.config_action_key_provider import ConfigActionKeyProvider
from digitalpy.config.configuration import Configuration
from digitalpy.core.event_manager import EventManager
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.routing.action_mapper import ActionMapper
from digitalpy.parsing.formatter import Formatter
from digitalpy.core.object_factory import ObjectFactory
import threading
import zmq


class AsyncActionMapper(ActionMapper):
    #
    # Constructor
    # @param session
    # @param permissionManager
    # @param eventManager
    # @param formatter
    # @param configuration
    #
    def __init__(
        self,
        event_manager: EventManager,
        configuration: Configuration,
        formatter: Formatter,
        routing_publisher_address,
        routing_subscriber_address,
    ):
        self.eventManager = event_manager
        self.configuration = configuration
        self.is_finished = False
        self.routing_publisher_address = routing_publisher_address
        self.routing_subscriber_address = routing_subscriber_address
        self.formatter = formatter
        self.initiate_sockets()

    def get_routing_publisher(self):
        sock_context = zmq.Context()
        routing_publisher = sock_context.socket(zmq.PUB)
        routing_publisher.connect(self.routing_subscriber_address)
        time.sleep(1)
        return routing_publisher

    def initiate_sockets(self):
        self.sock_context = zmq.Context()
        self.routing_publisher = self.sock_context.socket(zmq.PUB)
        self.routing_publisher.connect(self.routing_subscriber_address)
        self.general_routing_subscriber = self.sock_context.socket(zmq.SUB)
        self.general_routing_subscriber.connect(self.routing_publisher_address)

    def add_topic(self, topic):
        """this method is responsible for adding a new topic to the general_routing_subscriber"""
        self.general_routing_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)

    def get_responses(self) -> list:
        """this method is responsible for getting all the responses
        sent by the routing proxy and returning them in a list"""
        responses = []

        while True:
            try:
                message = self.general_routing_subscriber.recv_multipart(zmq.NOBLOCK)

            # handling the inevitable timeout exception when there are no responses
            # to be received at which point the list of responses will be returned
            except Exception as e:
                return responses

            # instantiate the response object
            response = ObjectFactory.get_instance("response")
            response.set_format("pickled")

            # get the values returned from the routing proxy and serialize them to
            values = message[1]
            response.set_values(values)
            self.formatter.deserialize(response)

            topic = message[0]
            topic_sections = topic.decode("utf-8").split("/")
            response.set_sender(topic_sections[4])
            response.set_context(topic_sections[5])
            response.set_action(topic_sections[6])

            responses.append(response)

    def get_response(
        self, response: Response, request: Request, listener: zmq.Socket, timeout=10000
    ):
        try:
            topic = f"/routing/response/{request.get_sender()}/{request.get_context()}/{request.get_action()}/{request.get_format()}/{request.get_id()}"
            listener.RCVTIMEO = timeout
            messages = listener.recv_multipart()
            listener.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            values = messages[1]
            response.set_values(values)
            self.formatter.deserialize(response)
            return response
        except Exception as e:
            listener.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            # temporary fix to see if delay is required before closing the socket
            import time

            time.sleep(3)
            print(e)
            listener.close()
            pass

    #
    # @see ActionMapper.processAction()
    #
    def process_action(
        self, request: Request, response: Response, return_listener: bool
    ):
        self.eventManager.dispatch(
            ApplicationEvent.NAME,
            ApplicationEvent(ApplicationEvent.BEFORE_ROUTE_ACTION, request),
        )

        referrer = request.get_sender()
        context = request.get_context()
        action = request.get_action()
        response.set_sender(referrer)
        response.set_context(context)
        response.set_action(action)

        self.formatter.serialize(request)

        if return_listener:
            topic = f"/routing/response/{request.get_sender()}/{request.get_context()}/{request.get_action()}/{request.get_format()}/{request.get_id()}"
            routing_subscriber = zmq.Context().socket(zmq.SUB)
            routing_subscriber.connect(self.routing_publisher_address)
            routing_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)
        else:
            routing_subscriber = None

        self.submit_request(request)

        return routing_subscriber

    def submit_request(self, request):
        with self.get_routing_publisher() as routing_publisher:
            routing_publisher.send_multipart(
                [
                    f"/routing/request/{request.get_sender()}/{request.get_context()}/{request.get_action()}/{request.get_format()}/{request.get_id()}".encode(
                        "utf-8"
                    ),
                    request.get_values(),
                ]
            )

    def __getstate__(self):
        self.routing_publisher.close()
        self.general_routing_subscriber.close()
        self.sock_context.term()
        state = self.__dict__.copy()
        del state["routing_publisher"]
        del state["general_routing_subscriber"]
        del state["sock_context"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.initiate_sockets()
