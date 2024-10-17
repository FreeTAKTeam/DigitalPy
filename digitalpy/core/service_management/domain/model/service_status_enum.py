"""This module contains the possible states of a service."""
from enum import Enum

class ServiceStatusEnum(Enum):
    """This class contains the possible states of a service."""
    # a state where the service is completely running
    RUNNING = "RUNNING"
    # a state where the service is completely stopped
    STOPPED = "STOPPED"
    # the service state could not be determined
    UNKNOWN = "UNKNOWN"
    # the service is in an error state or has exited with an error
    ERROR = "ERROR"

    STOPPING = "STOPPING"