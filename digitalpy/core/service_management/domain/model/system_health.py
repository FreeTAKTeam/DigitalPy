"""
Module for managing SystemHealth configurations and their properties.

This module defines the SystemHealth class, which is a subclass of Node.
It is designed to handle system health-related data with attributes such as cpu,
disk, and memory.
"""

from digitalpy.core.domain.node import Node

class SystemHealth(Node):
    """
    A class to represent System Health.

    Attributes:
        cpu (float): The CPU usage percentage.
        disk (float): The disk usage percentage.
        memory (float): The memory usage percentage.
    """
    
    def __init__(self, model_configuration, model, oid=None, node_type="SystemHealth") -> None:
        """
        Initializes the SystemHealth with the provided configuration, model, and optional ID.

        Args:
            model_configuration: The configuration for the model.
            model: The model associated with the system health.
            oid: Optional ID for the system health.
            node_type: The type of the node, default is "SystemHealth".
        """
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._cpu: float = None
        self._disk: float = None
        self._memory: float = None
        self._timestamp: str = None

    @property
    def cpu(self) -> float:
        """The CPU usage percentage."""
        return self._cpu
    
    @cpu.setter
    def cpu(self, cpu: float):
        cpu = float(cpu)
        if not isinstance(cpu, float):
            raise TypeError("'cpu' must be of type float")
        self._cpu = cpu

    @property
    def disk(self) -> float:
        """The disk usage percentage."""
        return self._disk
    
    @disk.setter
    def disk(self, disk: float):
        disk = float(disk)
        if not isinstance(disk, float):
            raise TypeError("'disk' must be of type float")
        self._disk = disk

    @property
    def memory(self) -> float:
        """The memory usage percentage."""
        return self._memory
    
    @memory.setter
    def memory(self, memory: float):
        memory = float(memory)
        if not isinstance(memory, float):
            raise TypeError("'memory' must be of type float")
        self._memory = memory

    @property
    def timestamp(self) -> str:
        """The timestamp of the system health data."""
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: str):
        if not isinstance(timestamp, str):
            raise TypeError("'timestamp' must be of type str")
        self._timestamp = timestamp