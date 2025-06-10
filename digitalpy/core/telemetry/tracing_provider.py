from abc import ABC, abstractmethod
from digitalpy.core.telemetry.tracer import Tracer

class TracingProvider(ABC):
    
    @abstractmethod
    def initialize_tracing(self):
        """Initialize the tracing provider."""

    @abstractmethod
    def create_tracer(self, tracer_name: str) -> Tracer:
        """Create a new tracer instance from the current tracer provider.

        Args:
            tracer_name (str): The name to associate with the tracer instance.

        Returns:
            Tracer: A new tracer instance with the given name.
        """
