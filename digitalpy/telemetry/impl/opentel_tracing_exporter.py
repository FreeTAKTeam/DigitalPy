from digitalpy.telemetry.tracing_exporter import TracingExporter
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
import json

class OpenTelTracingExporter(TracingExporter):
    def __init__(self, exporter: InMemorySpanExporter):
        self.exporter = exporter
    
    def get_spans(self):
        output_spans = []
        for span in self.exporter.get_finished_spans():
            output_spans.append(json.loads(span.to_json()))
        return output_spans