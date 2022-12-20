from abc import ABC, abstractmethod

class Service(ABC):
    def __init__(self):
        self.running = True
    
    @abstractmethod
    def server(self):
        """this property should be used to accept connections and send messages"""
    
    @abstractmethod
    def start(self):
        """this method should be used to start the service as a process"""
    
    @abstractmethod
    def stop(self):
        """this method should be used to stop the service and the process its running in"""
    
    @abstractmethod
    def send_message(self, message, client):
        """this method should be used to send a message to a client"""
    
    @abstractmethod
    def receive_message(self, client):
        """this method should be used to receive a message from a client"""