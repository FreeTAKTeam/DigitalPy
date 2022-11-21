from digitalpy.telemetry.impl.opentel_tracer import OpenTelTracer
from digitalpy.telemetry.tracing_provider import TracingProvider
from opentelemetry.sdk.trace import TracerProvider
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.telemetry.impl.opentel_tracing_exporter import OpenTelTracingExporter

class OpenTelTracingProvider(TracingProvider):
    """tracing provider implementation for the open telemetry protocol.
    """
    def __init__(self):
        self.provider = TracerProvider()
        exporter = ObjectFactory.get_instance("TracerExporter")
        self.exporter = OpenTelTracingExporter(exporter)
        self.processor = ObjectFactory.get_instance("TracerProcessor", dynamic_configuration={"span_exporter": exporter})
        self.provider.add_span_processor(self.processor)
        
    def create_tracer(self, tracer_name: str) -> OpenTelTracer:
        """create a new OpenTelTracer instance

        Args:
            tracer_name (str): the name of the tracer to be created

        Returns:
            OpenTelTracer: an open telemetry tracer instance
                from the current provider instance with the passed name
        """
        return OpenTelTracer(self.provider.get_tracer(tracer_name))
