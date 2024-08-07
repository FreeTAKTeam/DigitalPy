"""
Module for managing ServiceStatus configurations and their properties.

This module defines the ServiceStatus class, which is a subclass of Node.
It is designed to handle service status-related data with attributes such as port,
service_name, service_status, and service_status_actual.
"""

from digitalpy.core.domain.node import Node

class ServiceStatus(Node):
    """
    A class to represent the status of a service.

    Attributes:
        port (int): The port number on which the service is running.
        service_name (str): The name of the service.
        service_status (str): The current status of the service.
        service_status_actual (str): The actual status of the service.
    """
    
    def __init__(self, model_configuration, model, oid=None, node_type="ServiceStatus") -> None:
        """
        Initializes the ServiceStatus with the provided configuration, model, and optional ID.

        Args:
            model_configuration: The configuration for the model.
            model: The model associated with the service status.
            oid: Optional ID for the service status.
            node_type: The type of the node, default is "ServiceStatus".
        """
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._port: int = None
        self._service_name: str = None
        self._service_status: str = None
        self._service_status_actual: str = None

    @property
    def port(self) -> int:
        """The port number on which the service is running."""
        return self._port
    
    @port.setter
    def port(self, port: int):
        port = int(port)
        if not isinstance(port, int):
            raise TypeError("'port' must be of type int")
        self._port = port

    @property
    def service_name(self) -> str:
        """The name of the service."""
        return self._service_name
    
    @service_name.setter
    def service_name(self, service_name: str):
        if not isinstance(service_name, str):
            raise TypeError("'service_name' must be of type str")
        self._service_name = service_name

    @property
    def service_status(self) -> str:
        """The current status of the service."""
        return self._service_status
    
    @service_status.setter
    def service_status(self, service_status: str):
        if not isinstance(service_status, str):
            raise TypeError("'service_status' must be of type str")
        self._service_status = service_status

    @property
    def service_status_actual(self) -> str:
        """The actual status of the service."""
        return self._service_status_actual
    
    @service_status_actual.setter
    def service_status_actual(self, service_status_actual: str):
        if not isinstance(service_status_actual, str):
            raise TypeError("'service_status_actual' must be of type str")
        self._service_status_actual = service_status_actual
