from digitalpy.telemetry.impl.opentel_meter import OpenTelMeter
from digitalpy.telemetry.impl.opentel_metric_reader import OpenTelMetricReader
from digitalpy.telemetry.metrics_provider import MetricsProvider
from digitalpy.core.object_factory import ObjectFactory
import io
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


class OpenTelMetricsProvider(MetricsProvider):
    """create an opentelemetry provider instance from which meter instances can be created"""

    def __init__(self, service_name):
        resource = Resource(attributes={SERVICE_NAME: service_name})
        try:
            reader = ObjectFactory.get_instance("MetricsReader")
        # handle the case where the reader requires a defined exporter
        except TypeError:
            self.exporter = ObjectFactory.get_instance("MetricsExporter")
            reader = ObjectFactory.get_instance(
                "MetricsReader", dynamic_configuration={"exporter": self.exporter}
            )
        self.provider = MeterProvider(resource=resource, metric_readers=[reader])
        self.reader = OpenTelMetricReader(reader)
        
    def create_meter(self, meter_name: str) -> OpenTelMeter:
        """instantiate an opentelemetry meter instance"""
        return OpenTelMeter(self.provider.get_meter(meter_name))
