"""
This module defines the ServiceOperations Enum class which represents the different operations
that can be performed on a service.

Classes:
    ServiceOperations: An enumeration of the different operations 
    that can be performed on a service.
"""

from enum import Enum

class ServiceCommands(Enum):
    """
    """
    GET_HEALTH = "get_health"
    STOP = "stop_service"
    GET_TOPICS = "get_topics"
    ADD_TOPIC = "add_topic"
    REMOVE_TOPIC = "remove_topic"