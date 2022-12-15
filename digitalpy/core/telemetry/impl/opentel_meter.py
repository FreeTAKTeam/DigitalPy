# used for type hinting to prevent circular import
from __future__ import annotations
from typing import TYPE_CHECKING
from digitalpy.telemetry.impl.opentel_counter import OpenTelCounter

if TYPE_CHECKING:
    from digitalpy.telemetry.impl.opentel_metrics_provider import OpenTelMetricsProvider

from digitalpy.core.telemetry.meter import Meter


class OpenTelMeter(Meter):
    def __init__(self, meter: OpenTelMeter) -> None:
        self.meter = meter

    def create_counter(self, name, description, unit) -> OpenTelCounter:
        """create a new open telemetry counter instance and return it"""
        return OpenTelCounter(self.meter.create_counter(name, description, unit))
