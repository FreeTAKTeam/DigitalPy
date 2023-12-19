
from enum import Enum

class ServiceStatus(Enum):
    RUNNING = "Running"
    # a state where the service is completely stopped
    STOPPED = "Stopped"
    # an intermediate state between running and stopped to allow for a clean shutdown
    STOPPING = "Stopping"
    PAUSED = "Paused"
    UNKNOWN = "Unknown"
    ERROR = "Error"
    DEAD = "Dead"
