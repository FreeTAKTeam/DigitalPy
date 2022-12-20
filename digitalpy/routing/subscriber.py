from abc import ABC, abstractmethod

class Subscriber(ABC):
    @abstractmethod
    def handle_sub_message(self, message):
        """handle the case where a subscriber message is received"""

    @abstractmethod
    def broker_receive(self):
        """Returns the reply message or None if there was no reply
        """
    
    @abstractmethod
    def broker_send(self, message):
        """Send request to broker
        """
        
    @abstractmethod
    def broker_connect(self, integration_manager_address: str, integration_manager_port: int, service_identity: str):
        """Connect or reconnect to broker
        """