from abc import ABC, abstractmethod

class Tracer(ABC):
    
    @abstractmethod
    def start_as_current_span(self, span_name: str):
        """this really isnt an abstractmethod however the telemetry system needs to
        move forward so at least this way refrences can be identified and replaced
        when/if the time comes that opentelemetry is no longer the target telemetry
        technology."""