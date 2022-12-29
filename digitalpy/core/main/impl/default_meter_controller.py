from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.telemetry.metrics_provider import MetricsProvider
from digitalpy.core.telemetry.meter import Meter


class MeterController(Controller):
    """essentially a wrapper around a given metrics object to enable
    different implementations of the Metrics object to be used dynamically."""

    def __init__(
        self, service_name, file_path, request, response, action_mapper, configuration
    ):
        super().__init__(request, response, action_mapper, configuration)
        self.service_name = service_name
        self.file_path = file_path
        self.provider: MetricsProvider = ObjectFactory.get_instance(
            f"metrics_provider_instance",
        )
        self.meter: Meter = self.provider.create_meter(service_name)

    def execute(self, method=None, **kwargs):
        """execute a given request method"""

        # if the method is a member of the current class then execute
        if hasattr(self, method):
            getattr(self, method)(**kwargs)
        # otherwise try to execute the operation on the metrics class
        else:
            getattr(self.meter, method)(**kwargs)

    def get_meter(self):
        """get the current meter instance."""
        self.request.set_value("meter", self.meter)

    def get_metrics(self):
        self.response.set_value("metrics", self.provider.reader.get_metrics())

    def reload_meter(self, service_name=None):
        """reload the current meter instance"""
        if service_name is None:
            service_name = self.service_name
        self.service_name = service_name
        self.provider: MetricsProvider = ObjectFactory.get_instance(
            f"metrics_provider_instance",
        )
        self.meter: Meter = self.provider.create_meter(service_name)
