"""This module provides a singleton class for managing metrics, service statuses,
system events, system health, and system logs.
"""

from typing import Dict, List, Optional
from digitalpy.core.telemetry.domain.metric import Metric
from digitalpy.core.telemetry.domain.service_status import ServiceStatus
from digitalpy.core.telemetry.domain.status_factory import StatusFactory
from digitalpy.core.telemetry.domain.system_event import SystemEvent
from digitalpy.core.telemetry.domain.system_health import SystemHealth
from digitalpy.core.telemetry.domain.system_log import SystemLog


class StatusFactorySingleton:
    """
    A singleton class for managing metrics, service statuses, system events, system health, 
    and system logs. This class provides methods for adding, retrieving, removing, and 
    clearing various types of objects in the factory.
    """

    __factory: StatusFactory = None

    @staticmethod
    def add_metric(metric: Metric) -> None:
        """Add a metric to the factory.

        Args:
            metric: The metric to add.
        """
        StatusFactorySingleton.__factory.add_metric(metric)

    @staticmethod
    def get_new_metric() -> Metric:
        """Get a new instance of a metric.

        Returns:
            Metric: A new instance of a metric.
        """
        return StatusFactorySingleton.__factory.get_new_metric()

    @staticmethod
    def get_metric(name: str) -> Optional[Metric]:
        """Get a metric by name, or None if not found.

        Args:
            name: The name of the metric to get.

        Returns:
            Optional[Metric]: The metric with the provided name, or None if not found

        """
        return StatusFactorySingleton.__factory.get_metric(name)

    @staticmethod
    def remove_metric(name: str) -> Optional[Metric]:
        """Remove a metric by name, or None if not found.

        Args:
            name: The name of the metric to remove.

        Returns:
            Optional[Metric]: The metric with the provided name, or None if not found

        """
        return StatusFactorySingleton.__factory.remove_metric(name)

    @staticmethod
    def get_metrics() -> Dict[str, Metric]:
        """Get all metrics in the factory.

        Returns:
            Dict[str, Metric]: A dictionary of all metrics in the factory.

        """
        return StatusFactorySingleton.__factory.get_metrics()

    @staticmethod
    def clear_metrics() -> None:
        """Clear all metrics from the factory."""
        StatusFactorySingleton.__factory.clear_metrics()

    @staticmethod
    def add_service_status(service_status: ServiceStatus) -> None:
        """Add a service status to the factory.

        Args:
            service_status: The service status to add.
        """
        StatusFactorySingleton.__factory.add_service_status(service_status)

    @staticmethod
    def get_new_service_status() -> ServiceStatus:
        """Get a new instance of a service status.

        Returns:
            ServiceStatus: A new instance of a service status.
        """
        return StatusFactorySingleton.__factory.get_new_service_status()

    @staticmethod
    def get_service_status(name: str) -> Optional[ServiceStatus]:
        """Get a service status by name, or None if not found.

        Args:
            name: The name of the service status to get.

        Returns:
            Optional[ServiceStatus]: The service status with the provided name, or None if not found

        """
        return StatusFactorySingleton.__factory.get_service_status(name)

    @staticmethod
    def remove_service_status(name: str) -> Optional[ServiceStatus]:
        """Remove a service status by name, or None if not found.

        Args:
            name: The name of the service status to remove.

        Returns:
            Optional[ServiceStatus]: The service status with the provided name, or None if not found

        """
        return StatusFactorySingleton.__factory.remove_service_status(name)

    @staticmethod
    def get_service_statuses() -> Dict[str, ServiceStatus]:
        """Get all service statuses in the factory.

        Returns:
            Dict[str, ServiceStatus]: A dictionary of all service statuses in the factory.

        """
        return StatusFactorySingleton.__factory.get_service_statuses()

    @staticmethod
    def clear_service_statuses() -> None:
        """Clear all service statuses from the factory."""
        StatusFactorySingleton.__factory.clear_service_statuses()

    @staticmethod
    def add_system_event(system_event: SystemEvent) -> None:
        """
        Add a system event to the factory.

        Args:
            system_event: The system event to be added.
        """
        StatusFactorySingleton.__factory.add_system_event(system_event)

    @staticmethod
    def get_system_events() -> List[SystemEvent]:
        """
        Retrieve all system events from the factory.

        Returns:
            List[SystemEvent]: A list of system events.
        """
        return StatusFactorySingleton.__factory.get_system_events()

    @staticmethod
    def clear_system_events() -> None:
        """
        Clear all system events from the factory.
        """
        StatusFactorySingleton.__factory.clear_system_events()

    @staticmethod
    def set_system_health(system_health: SystemHealth) -> None:
        """
        Set the system health status in the factory.

        Args:
            system_health: The system health status to be set.
        """
        StatusFactorySingleton.__factory.set_system_health(system_health)

    @staticmethod
    def get_system_health() -> SystemHealth:
        """
        Retrieve the system health status from the factory.

        Returns:
            SystemHealth: The current system health status.
        """
        return StatusFactorySingleton.__factory.get_system_health()

    @staticmethod
    def add_system_log(system_log: SystemLog) -> None:
        """
        Add a system log to the factory.

        Args:
            system_log: The system log to be added.
        """
        StatusFactorySingleton.__factory.add_system_log(system_log)

    @staticmethod
    def get_system_logs() -> List[SystemLog]:
        """
        Retrieve all system logs from the factory.

        Returns:
            List[SystemLog]: A list of system logs.
        """
        return StatusFactorySingleton.__factory.get_system_logs()

    @staticmethod
    def clear_system_logs() -> None:
        """
        Clear all system logs from the factory.
        """
        StatusFactorySingleton.__factory.clear_system_logs()
