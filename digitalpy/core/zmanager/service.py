from abc import ABC, abstractmethod

class Service(ABC):
    def __init__(self):
        self.running = True
    
    @abstractmethod
    def discovery(self):
        """used to  inform the discoverer of the specifics of this service"""
        # TODO: the contract for discovery needs to be established
        
    @abstractmethod
    def send_heart_beat(self):
        """send a heartbeat to inform the the service manager that it's alive"""

    @abstractmethod
    def start(self):
        """this method should be used to start the service as a process"""
    
    @abstractmethod
    def stop(self):
        """this method should be used to stop the service and the process its running in"""
    