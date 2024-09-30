from importlib import import_module
from typing import Optional
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.service_management.domain.model.system_log import SystemLog
from digitalpy.core.service_management.domain.model.system_health import SystemHealth
from digitalpy.core.service_management.domain.model.system_event import SystemEvent
from digitalpy.core.service_management.domain.model.service_status import ServiceStatus
from digitalpy.core.telemetry.domain.model.metric import Metric
from digitalpy.core.domain.node import Node

ServiceStatusClass = ServiceStatus

class StatusFactory:
    """StatusFactory class to create and retrieve status objects."""

    def __init__(self) -> None:
        self._metrics: dict[str, Metric] = {}
        self._service_statuses: dict[str, ServiceStatus] = {}
        self._system_events: list[SystemEvent] = []
        self._system_health: SystemHealth = SystemHealth(None, None)
        self._system_logs: list[SystemLog] = []

    def add_configuration(self, configuration: Configuration):
        """Add a configuration to the factory.
        
        Args:
            configuration: The configuration to add.
        """
        for section in configuration.get_sections():
            self._add_status_object(configuration.get_section(section))
                
    def _add_status_object(self, section: dict):
        """Get a new instance of a status object based on it's dictionary repr.
        This assumes that the dict repr contains all required fields to create the object.
        
        Args:
            section: The dictionary representation of the status object.
        """
        if section.get("__class", None) is None:
            return None

        status_class = self._import_class(section["__class"])
        status_object = status_class(None, None)
        propeties = status_object.get_properties()
        for key in section:
            if key in propeties:
                setattr(status_object, key, section[key])

        # TODO: This is a temporary solution. This should be refactored to using a proper pattern
        # not a switch statement.
        if isinstance(status_object, Metric):
            self.add_metric(status_object)
        elif isinstance(status_object, ServiceStatus):
            self.add_service_status(status_object)
        elif isinstance(status_object, SystemEvent):
            self.add_system_event(status_object)
        elif isinstance(status_object, SystemHealth):
            self.set_system_health(status_object)
        elif isinstance(status_object, SystemLog):
            self.add_system_log(status_object)
        
    def _import_class(self, class_name: str) -> type[Node]:
        """Import a class."""
        parts = class_name.split(".")
        module = import_module(".".join(parts[:-1]))
        return getattr(module, parts[-1])
        
    def _build_metric(self, section: dict) -> Metric:
        """Build a metric object from a dictionary representation.
        
        Args:
            section: The dictionary representation of the metric object.
        
        Returns:
            Metric: The built metric object.
        
        """
        return Metric(section["metric_name"], section["value"])

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
        self._service_statuses[service_status.service_name] = service_status

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