"""
Module for managing Metric configurations and their properties.

This module defines the Metric class, which is a subclass of Node.
It is designed to handle metric-related data with attributes such as description,
ID, metric_name, timestamp, unit, value, and value_expected.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from digitalpy.core.domain.node import Node


class Metric(Node):
    """
    A class to represent a Metric.

    Attributes:
        description (Optional[str]): A brief description of the metric.
        ID (UUID): The unique identifier for the metric.
        metric_name (str): The name of the metric.
        timestamp (datetime): The timestamp when the metric was recorded.
        unit (Optional[int]): The unit of the metric.
        value (int): The value of the metric.
        value_expected (Optional[int]): The expected value of the metric.
    """
    
    def __init__(self, model_configuration, model, oid=None, node_type="Metric") -> None:
        """
        Initializes the Metric with the provided configuration, model, and optional ID.

        Args:
            model_configuration: The configuration for the model.
            model: The model associated with the metric.
            oid: Optional ID for the metric.
            node_type: The type of the node, default is "Metric".
        """
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._description: Optional[str] = None
        self._ID: UUID = None
        self._metric_name: str = None
        self._timestamp: datetime = None
        self._unit: Optional[int] = None
        self._value: int = None
        self._value_expected: Optional[int] = None

    @property
    def description(self) -> Optional[str]:
        """A brief description of the metric."""
        return self._description
    
    @description.setter
    def description(self, description: Optional[str]):
        if description is not None and not isinstance(description, str):
            raise TypeError("'description' must be of type str or None")
        self._description = description

    @property
    def ID(self) -> UUID:
        """The unique identifier for the metric."""
        return self._ID
    
    @ID.setter
    def ID(self, ID: UUID):
        if not isinstance(ID, UUID):
            raise TypeError("'ID' must be of type UUID")
        self._ID = ID

    @property
    def metric_name(self) -> str:
        """The name of the metric."""
        return self._metric_name
    
    @metric_name.setter
    def metric_name(self, metric_name: str):
        if not isinstance(metric_name, str):
            raise TypeError("'metric_name' must be of type str")
        self._metric_name = metric_name

    @property
    def timestamp(self) -> datetime:
        """The timestamp when the metric was recorded."""
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        if not isinstance(timestamp, datetime):
            raise TypeError("'timestamp' must be of type datetime")
        self._timestamp = timestamp

    @property
    def unit(self) -> Optional[int]:
        """The unit of the metric."""
        return self._unit
    
    @unit.setter
    def unit(self, unit: Optional[int]):
        if unit is not None and not isinstance(unit, int):
            raise TypeError("'unit' must be of type int or None")
        self._unit = unit

    @property
    def value(self) -> int:
        """The value of the metric."""
        return self._value
    
    @value.setter
    def value(self, value: int):
        if not isinstance(value, int):
            raise TypeError("'value' must be of type int")
        self._value = value

    @property
    def value_expected(self) -> Optional[int]:
        """The expected value of the metric."""
        return self._value_expected
    
    @value_expected.setter
    def value_expected(self, value_expected: Optional[int]):
        if value_expected is not None and not isinstance(value_expected, int):
            raise TypeError("'value_expected' must be of type int or None")
        self._value_expected = value_expected
