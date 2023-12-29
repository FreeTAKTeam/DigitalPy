from enum import Enum

class ServiceHealthCategory(Enum):
    """Service Health Category"""
    # the service is operational with all metrics in acceptable ranges
    OPERATIONAL = "Operational"
    # some or all metrics are outside of acceptable ranges
    DEGRADED = "Degraded"
    # the service is not responding to requests
    UNRESPONSIVE = "Unresponsive"