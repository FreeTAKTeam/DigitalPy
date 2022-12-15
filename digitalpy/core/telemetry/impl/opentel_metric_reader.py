from opentelemetry.sdk.metrics.export import MetricReader as OpenTelMetricReaderImpl
import json
from digitalpy.core.telemetry.metrics_reader import MetricReader


class OpenTelMetricReader(MetricReader):
    def __init__(self, metric_reader: OpenTelMetricReaderImpl):
        self.metric_reader = metric_reader

    def get_metrics(self) -> dict:
        """returns a dictionary of metrics from the current metric reader"""
        return json.loads(self.metric_reader.get_metrics_data().to_json())
