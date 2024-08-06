"""
Module for managing SystemLog configurations and their properties.

This module defines the SystemLog class, which is a subclass of Node.
It is designed to handle system log-related data with attributes such as file,
message, name, severity, and timestamp.
"""

from typing import Optional

from digitalpy.core.domain.node import Node


class SystemLog(Node):
    """
    A class to represent a System Log.

    Attributes:
        file (Optional[str]): The file associated with the log.
        message (str): The message contained in the log.
        name (Optional[str]): The name of the log.
        severity (str): The severity level of the log.
        timestamp (str): The timestamp when the log was created.
    """
    
    def __init__(self, model_configuration, model, oid=None, node_type="SystemLog") -> None:
        """
        Initializes the SystemLog with the provided configuration, model, and optional ID.

        Args:
            model_configuration: The configuration for the model.
            model: The model associated with the system log.
            oid: Optional ID for the system log.
            node_type: The type of the node, default is "SystemLog".
        """
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._file: Optional[str] = None
        self._message: str = None
        self._name: Optional[str] = None
        self._severity: str = None
        self._timestamp: str = None

    @property
    def file(self) -> Optional[str]:
        """The file associated with the log."""
        return self._file
    
    @file.setter
    def file(self, file: Optional[str]):
        if file is not None and not isinstance(file, str):
            raise TypeError("'file' must be of type str or None")
        self._file = file

    @property
    def message(self) -> str:
        """The message contained in the log."""
        return self._message
    
    @message.setter
    def message(self, message: str):
        if not isinstance(message, str):
            raise TypeError("'message' must be of type str")
        self._message = message

    @property
    def name(self) -> Optional[str]:
        """The name of the log."""
        return self._name
    
    @name.setter
    def name(self, name: Optional[str]):
        if name is not None and not isinstance(name, str):
            raise TypeError("'name' must be of type str or None")
        self._name = name

    @property
    def severity(self) -> str:
        """The severity level of the log."""
        return self._severity
    
    @severity.setter
    def severity(self, severity: str):
        if not isinstance(severity, str):
            raise TypeError("'severity' must be of type str")
        self._severity = severity

    @property
    def timestamp(self) -> str:
        """The timestamp when the log was created."""
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: str):
        if not isinstance(timestamp, str):
            raise TypeError("'timestamp' must be of type str")
        self._timestamp = timestamp
