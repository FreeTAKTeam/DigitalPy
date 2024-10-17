"""
Module for managing SystemEvent configurations and their properties.

This module defines the SystemEvent class, which is a subclass of Node.
It is designed to handle system event-related data with attributes such as event_id,
message, and source.
"""

from digitalpy.core.domain.node import Node
from uuid import UUID

class SystemEvent(Node):
    """
    A class to represent a System Event.

    Attributes:
        event_id (UUID): The unique identifier for the event.
        message (str): The message associated with the event.
        source (str): The source of the event.
    """
    
    def __init__(self, model_configuration, model, oid=None, node_type="SystemEvent") -> None:
        """
        Initializes the SystemEvent with the provided configuration, model, and optional ID.

        Args:
            model_configuration: The configuration for the model.
            model: The model associated with the system event.
            oid: Optional ID for the system event.
            node_type: The type of the node, default is "SystemEvent".
        """
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._event_id: UUID = None
        self._message: str = None
        self._source: str = None

    @property
    def event_id(self) -> UUID:
        """The unique identifier for the event."""
        return self._event_id
    
    @event_id.setter
    def event_id(self, event_id: UUID):
        if not isinstance(event_id, UUID):
            raise TypeError("'event_id' must be of type UUID")
        self._event_id = event_id

    @property
    def message(self) -> str:
        """The message associated with the event."""
        return self._message
    
    @message.setter
    def message(self, message: str):
        if not isinstance(message, str):
            raise TypeError("'message' must be of type str")
        self._message = message

    @property
    def source(self) -> str:
        """The source of the event."""
        return self._source
    
    @source.setter
    def source(self, source: str):
        if not isinstance(source, str):
            raise TypeError("'source' must be of type str")
        self._source = source
