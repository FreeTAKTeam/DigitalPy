from typing import Dict
from digitalpy.telemetry.counter import Counter


class OpenTelCounter(Counter):
    def __init__(self, counter):
        self.counter = counter

    def increment(self, value: int, labels: Dict[str, str]):
        self.counter.add(value, labels)
