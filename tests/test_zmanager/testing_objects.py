from dataclasses import dataclass


@dataclass
class PerformanceTestResults:
    message_count: int
    total_time: float
    worker_count: int
    service_count: int
    worker_class: str
