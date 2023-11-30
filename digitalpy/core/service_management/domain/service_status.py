
from enum import Enum

class ServiceStatus(Enum):
    RUNNING = "Running"
    STOPPED = "Stopped"
    PAUSED = "Paused"
    UNKNOWN = "Unknown"
