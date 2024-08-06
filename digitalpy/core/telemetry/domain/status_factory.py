from typing import Optional
from digitalpy.core.telemetry.domain.system_log import SystemLog
from digitalpy.core.telemetry.domain.system_health import SystemHealth
from digitalpy.core.telemetry.domain.system_event import SystemEvent
from digitalpy.core.telemetry.domain.service_status import ServiceStatus
from digitalpy.core.telemetry.domain.metric import Metric


class StatusFactory:
    """StatusFactory class to create and retrieve status objects."""

    def __init__(self) -> None:
        self._metrics: dict[str, Metric]
        self._service_statuses: dict[str, ServiceStatus]
        self._system_events: list[SystemEvent]
        self._system_health: SystemHealth
        self._system_logs: list[SystemLog]

    def add_metric(self, metric: Metric):
        """Add a metric to the factory.
        
        Args:
            metric: The metric to add.
        """
        self._metrics[metric.metric_name] = metric

    def get_new_metric(self) -> Metric:
        """Get a new instance of a metric.
        
        Returns:
            Metric: A new instance of a metric.
        """
        return Metric(None, None)

    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name, or None if not found.
        
        Args:
            name: The name of the metric to get.

        Returns:
            Optiona[Metric]: The metric with the provided name, or None if not found
        
        """
        return self._metrics.get(name, None)
    
    def remove_metric(self, name: str) -> Optional[Metric]:
        """Remove a metric by name, or None if not found.
        
        Args:
            name: The name of the metric to remove.

        Returns:
            Optiona[Metric]: The metric with the provided name, or None if not found
        
        """
        return self._metrics.pop(name, None)
    
    def get_metrics(self) -> dict[str, Metric]:
        """Get all metrics in the factory.
        
        Returns:
            dict[str, Metric]: A dictionary of all metrics in the factory.
        
        """
        return self._metrics
    
    def clear_metrics(self):
        """Clear all metrics from the factory."""
        self._metrics.clear()

    def add_service_status(self, service_status: ServiceStatus):
        """Add a service status to the factory.
        
        Args:
            service_status: The service status to add.
        """
        self._service_statuses[service_status.status_name] = service_status

    def get_new_service_status(self) -> ServiceStatus:
        """Get a new instance of a service status.
        
        Returns:
            ServiceStatus: A new instance of a service status.
        """
        return ServiceStatus(None, None)

    def get_service_status(self, name: str) -> Optional[ServiceStatus]:
        """Get a service status by name, or None if not found.
        
        Args:
            name: The name of the service status to get.

        Returns:
            Optional[ServiceStatus]: The service status with the provided name, or None if not found
        
        """
        return self._service_statuses.get(name, None)
    
    def remove_service_status(self, name: str) -> Optional[ServiceStatus]:
        """Remove a service status by name, or None if not found.
        
        Args:
            name: The name of the service status to remove.

        Returns:
            Optional[ServiceStatus]: The service status with the provided name, or None if not found
        
        """
        return self._service_statuses.pop(name, None)
    
    def get_service_statuses(self) -> dict[str, ServiceStatus]:
        """Get all service statuses in the factory.
        
        Returns:
            dict[str, ServiceStatus]: A dictionary of all service statuses in the factory.
        
        """
        return self._service_statuses
    
    def clear_service_statuses(self):
        """Clear all service statuses from the factory."""
        self._service_statuses.clear()
    
    def add_system_event(self, system_event: SystemEvent):
        """Add a system event to the factory.
        
        Args:
            system_event: The system event to add.
        """
        self._system_events.append(system_event)
    
    def get_system_events(self) -> list[SystemEvent]:
        """Get all system events in the factory.
        
        Returns:
            list[SystemEvent]: A list of all system events in the factory.
        
        """
        return self._system_events
    
    def clear_system_events(self):
        """Clear all system events from the factory."""
        self._system_events.clear()
    
    def set_system_health(self, system_health: SystemHealth):
        """Set the system health in the factory.
        
        Args:
            system_health: The system health to set.
        """
        self._system_health = system_health
    
    def get_system_health(self) -> SystemHealth:
        """Get the system health from the factory.
        
        Returns:
            SystemHealth: The system health in the factory.
        
        """
        return self._system_health
    
    def add_system_log(self, system_log: SystemLog):
        """Add a system log to the factory.
        
        Args:
            system_log: The system log to add.
        """
        self._system_logs.append(system_log)
    
    def get_system_logs(self) -> list[SystemLog]:
        """Get all system logs in the factory.
        
        Returns:
            list[SystemLog]: A list of all system logs in the factory.
        
        """
        return self._system_logs
    
    def clear_system_logs(self):
        """Clear all system logs from the factory."""
        self._system_logs.clear()