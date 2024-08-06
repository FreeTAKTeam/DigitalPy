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
        cpu (int): The CPU usage percentage.
        disk (int): The disk usage percentage.
        memory (int): The memory usage percentage.
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
        self._cpu: int = None
        self._disk: int = None
        self._memory: int = None

    @property
    def cpu(self) -> int:
        """The CPU usage percentage."""
        return self._cpu
    
    @cpu.setter
    def cpu(self, cpu: int):
        if not isinstance(cpu, int):
            raise TypeError("'cpu' must be of type int")
        self._cpu = cpu

    @property
    def disk(self) -> int:
        """The disk usage percentage."""
        return self._disk
    
    @disk.setter
    def disk(self, disk: int):
        if not isinstance(disk, int):
            raise TypeError("'disk' must be of type int")
        self._disk = disk

    @property
    def memory(self) -> int:
        """The memory usage percentage."""
        return self._memory
    
    @memory.setter
    def memory(self, memory: int):
        if not isinstance(memory, int):
            raise TypeError("'memory' must be of type int")
        self._memory = memory
