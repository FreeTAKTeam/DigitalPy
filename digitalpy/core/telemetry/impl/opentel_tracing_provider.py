from digitalpy.core.telemetry.impl.opentel_tracer import OpenTelTracer
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from opentelemetry.sdk.trace import TracerProvider
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.telemetry.impl.opentel_tracing_exporter import (
    OpenTelTracingExporter,
)


class OpenTelTracingProvider(TracingProvider):
    """tracing provider implementation for the open telemetry protocol."""

    def initialize_tracing(self):
        self.provider = TracerProvider()
        exporter = ObjectFactory.get_new_instance("TracerExporter")
        self.exporter = OpenTelTracingExporter(exporter)
        self.processor = ObjectFactory.get_new_instance(
            "TracerProcessor", dynamic_configuration={"span_exporter": exporter}
        )
        self.provider.add_span_processor(self.processor)

    def create_tracer(self, tracer_name: str) -> OpenTelTracer:
        """create a new OpenTelTracer instance

        Args:
            tracer_name (str): the name of the tracer to be created

        Returns:
            OpenTelTracer: an open telemetry tracer instance
                from the current provider instance with the passed name
        """
        if not hasattr(self, "provider"):
            self.initialize_tracing()
        return OpenTelTracer(self.provider.get_tracer(tracer_name))

    # __getstate__ used to address the issue of passing a dictionary containing the
    # openteltracingprovider to a multiprocess, basically the shutdown
    # thread object still causes problems in the processor so deleting
    # the object every time a class instance is serialized
    # addresses the issue.

    def __getstate__(self):
        """get the state of the object in without un-serializable objects"""
        if hasattr(self, "provider"):
            self.provider.shutdown()
            del self.provider
        if hasattr(self, "processor"):
            self.processor.shutdown()
            del self.processor
        if hasattr(self, "exporter"):
            del self.exporter
        return self.__dict__
