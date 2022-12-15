from abc import ABC, abstractmethod
from digitalpy.core.telemetry.tracer import Tracer

class TracingProvider(ABC):
    
    @abstractmethod
    def create_tracer(self, tracer_name: str) -> Tracer:
        """create a new tracer instance from the current tracer provider

        Args:
            tracer_name (str): the name to associate with the tracer instance

        Returns:
            Tracer: a new tracer instance with the given name
        """        