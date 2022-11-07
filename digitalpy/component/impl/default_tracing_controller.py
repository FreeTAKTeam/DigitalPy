from digitalpy.routing.controller import Controller
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.telemetry.tracing_provider import TracingProvider
from digitalpy.telemetry.tracer import Tracer


class TracingController(Controller):
    """generic controller for implementation in every component to
    support tracing functionality.
    """

    def __init__(self, name, request, response, action_mapper, configuration):
        super().__init__(request, response, action_mapper, configuration)
        self.provider: TracingProvider = ObjectFactory.get_instance(
            f"tracing_provider_instance",
        )
        self.tracer: Tracer = self.provider.create_tracer(name)

    def execute(self, method=None, **kwargs):
        # if the method is a member of the current class then execute
        if hasattr(self, method):
            getattr(self, method)(**kwargs)
        # otherwise try to execute the operation on the tracer class
        else:
            getattr(self.tracer, method)(**kwargs)

    def get_traces(self):
        self.response.set_value("traces", self.provider.exporter.get_spans())

    def get_tracer(self):
        """get the current tracer instance."""
        return self.tracer

    def reload_tracer(self):
        """reload the current tracer instance."""
        self.provider: TracingProvider = ObjectFactory.get_instance(
            f"tracing_provider_instance",
        )
        self.tracer: Tracer = self.provider.create_tracer()
