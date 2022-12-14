from digitalpy.routing.subscriber import Subscriber
import zmq
class ZmqSubscriber(Subscriber):
    
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        
    def broker_connect(self, integration_manager_address: str, integration_manager_port: int, service_identity: str):
        """Connect or reconnect to broker
        """
        self.socket.connect(f"tcp://{integration_manager_address}:{integration_manager_port}")
        self.socket.setsockopt(zmq.SUBSCRIBE, service_identity)

    def broker_receive(self):
        """Returns the reply message or None if there was no reply
        """
        return self.socket.recv_multipart()

    def broker_send(self, message):
        """Send request to broker
        """
        self.socket.send(message)