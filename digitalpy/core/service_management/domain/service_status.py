"""This module contains the possible states of a service."""
# a state where the service is completely running
RUNNING = "RUNNING"
# a state where the service is completely stopped
STOPPED = "STOPPED"
# an intermediate state between running and stopped to allow for a clean shutdown
STOPPING = "STOPPING"
UNKNOWN = "UNKNOWN"
ERROR = "ERROR"
