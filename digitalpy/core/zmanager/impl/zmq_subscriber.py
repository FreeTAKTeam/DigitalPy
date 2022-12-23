import zmq
from typing import List

from digitalpy.core.zmanager.subscriber import Subscriber
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.formatter import Formatter

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
                decoded_topic = topic.decode("utf-8")
                topic_sections = decoded_topic.split("/")
                _, _, _, _, sender, context, action, *_ = topic_sections
                response.set_sender(sender)
                response.set_context(context)
                response.set_action(action)

                responses.append(response)

        except zmq.ZMQError:
            return responses

    def broker_send(self, message):
        """Send request to broker
        """
        self.socket.send(message)