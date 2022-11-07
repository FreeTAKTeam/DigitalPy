from opentelemetry.trace import Tracer as OpenTelTracerImpl
from digitalpy.telemetry.tracer import Tracer

class OpenTelTracer(Tracer):
    """class to implement the digitalpy Tracer interface for the 
    open telemetry Tracer object"""
    
    #TODO: figure out how to abstract more operations of the tracer
    def __init__(self, tracer: OpenTelTracerImpl):
        self.tracer = tracer
        
    def start_as_current_span(self, name: str):
        return self.tracer.start_as_current_span(name = name)