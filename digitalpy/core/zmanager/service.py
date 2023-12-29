from abc import ABC, abstractmethod

from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.telemetry.tracing_provider import TracingProvider

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
        # TODO: this is seemingly replaced by the implementation of the health check
        
    @abstractmethod
    def start(self, object_factory: DefaultFactory, tracing_provider: TracingProvider):
        """this method should be used to start the service as a process"""
    
    @abstractmethod
    def stop(self):
        """this method should be used to stop the service and the process its running in"""
    