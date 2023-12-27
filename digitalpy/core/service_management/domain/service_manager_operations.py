"""
This module defines the ServiceManagerOperations Enum class which represents the different 
operations that can be performed by a service manager.

Classes:
    ServiceManagerOperations: An enumeration of the different operations that can be 
    performed by a service manager.
"""

from enum import Enum


class ServiceManagerOperations(Enum):
    """
    A class used to represent the different operations that can be performed by a service manager.

    ...

    Attributes
    ----------
    START_SERVICE : str
        Represents the operation to start a service.
    STOP_SERVICE : str
        Represents the operation to stop a service.
    RESTART_SERVICE : str
        Represents the operation to restart a service.
    GET_ALL_SERVICE_HEALTH : str
        Represents the operation to get the health status of all services.

    Methods
    -------
    None
    """
    START_SERVICE = "start_service"
    STOP_SERVICE = "stop_service"
    RESTART_SERVICE = "restart_service"
    GET_ALL_SERVICE_HEALTH = "get_all_service_health"
