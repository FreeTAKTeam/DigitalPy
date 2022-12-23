import zmq
from typing import List

from digitalpy.routing.subscriber import Subscriber
from digitalpy.routing.response import Response
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.parsing.formatter import Formatter

class ZmqSubscriber(Subscriber):
    
    def __init__(self, formatter: Formatter):
        self.context = zmq.Context()
        self.formatter = formatter
        self.socket = self.context.socket(zmq.SUB)
        
    def broker_connect(self, integration_manager_address: str, integration_manager_port: int, service_identity: str):
        """Connect or reconnect to broker
        """
        self.socket.connect(f"tcp://{integration_manager_address}:{integration_manager_port}")
        self.socket.setsockopt(zmq.SUBSCRIBE, f"/{service_identity}/messages")
        self.socket.setsockopt(zmq.SUBSCRIBE, f"/{service_identity}/commands")
        
    def broker_receive(self) -> List[Response]:
        """Returns the reply message or None if there was no reply
        """
        responses = []
        try:
            while True:
                message = self.socket.recv_multipart(flags=zmq.NOBLOCK)
                # instantiate the response object
                response = ObjectFactory.get_instance("response")
                
                # TODO: this is assuming that the message from the integration manager is pickled
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

        except zmq.ZMQError:
            return responses

    def broker_send(self, message):
        """Send request to broker
        """
        self.socket.send(message)