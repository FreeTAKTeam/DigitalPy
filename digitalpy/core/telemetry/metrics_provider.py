from abc import ABC, abstractmethod

from digitalpy.core.telemetry.meter import Meter

class MetricsProvider(ABC):
    
    @abstractmethod
    def create_meter(self, meter_name: str) -> Meter:
        """instantiate and return a new meter"""