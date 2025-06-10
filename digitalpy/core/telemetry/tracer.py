from abc import ABC, abstractmethod
from typing import Any
class Tracer(ABC):

    @abstractmethod
    def start_as_current_span(self, span_name: str) -> Any:
        """Start a span and set it as the current one.

        This method is not truly abstract; however, the telemetry system
        requires it so that references can be identified and replaced if the
        time comes when OpenTelemetry is no longer the target technology.
        """
