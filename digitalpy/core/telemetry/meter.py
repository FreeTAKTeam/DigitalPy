# used for type hinting to prevent circular import
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from digitalpy.core.telemetry.counter import Counter
    from digitalpy.core.telemetry.metrics_provider import MetricsProvider

from abc import ABC, abstractmethod


class Meter(ABC):
        
    def __init__(self, provider: MetricsProvider, meter_name: str=None):
        """the constructor for the abstract meter class

        Args:
            provider (MetricsProvider): the metrics provider used to create this meter
            meter_name (str, optional): the name of this meter instance. Defaults to None.
        """
        if meter_name is None:
            meter_name = self.__class__.__name__
        self.meter = provider.get_meter(meter_name)
    
    @abstractmethod
    def create_counter(self, name, description, unit) -> Counter:
        """this method should instantiate a new counter object with 
        the passed values"""