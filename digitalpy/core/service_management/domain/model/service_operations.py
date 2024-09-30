"""
This module defines the ServiceOperations Enum class which represents the different operations
that can be performed on a service.

Classes:
    ServiceOperations: An enumeration of the different operations 
    that can be performed on a service.
"""

from enum import Enum

class ServiceOperations(Enum):
    """
    A class used to represent the different operations that can be performed on a service.

    ...

    Attributes
    ----------
    STOP : str
        Represents the operation to stop a service.
    STATUS : str
        Represents the operation to check the health status of a service.

    Methods
    -------
    None
    """
    GET_HEALTH = "get_health"
    STOP = "stop_service"