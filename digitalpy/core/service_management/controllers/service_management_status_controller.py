from typing import TYPE_CHECKING
import psutil

from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.service_management.domain.builder.service_status_builder import (
    ServiceStatusBuilder,
)
from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.service_management.persistence.service_status import ServiceStatus
from digitalpy.core.service_management.persistence.system_log import SystemLog
from digitalpy.core.service_management.domain.builder.system_health_builder import (
    SystemHealthBuilder,
)
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.singleton_status_factory import SingletonStatusFactory

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.domain.model.configuration import (
        Configuration,
    )
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
from datetime import datetime


class ServiceManagementStatusController(Controller):
    """This class is used to modify the status factory. It exposes methods to modify the attriubtes
    of the status factory."""

    def __init__(
        self,
        request: "Request",
        response: "Response",
        sync_action_mapper: "DefaultActionMapper",
        configuration: "Configuration",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.system_health_builder = SystemHealthBuilder(
            request, response, sync_action_mapper, configuration
        )
        self.service_status_builder = ServiceStatusBuilder(
            request, response, sync_action_mapper, configuration
        )

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller."""
        super().initialize(request, response)

    def reload_system_health(self, config_loader, *args, **kwargs):
        """This function is used to reload the system health by getting the current
        system information from the operating system."""
        # TODO: currently there is a duplicate of the model_definition between service_management and telemetry
        self.system_health_builder.build_empty_object(config_loader)
        system_health = self.system_health_builder.get_result()

        system_health.cpu = psutil.cpu_percent(interval=1)
        system_health.disk = psutil.disk_usage("/").percent
        system_health.memory = psutil.virtual_memory().percent
        system_health.timestamp = datetime.now().isoformat()

        SingletonStatusFactory.set_system_health(system_health)
        self.response.set_value("message", system_health)

    def add_system_log(self, system_log: SystemLog, *args, **kwargs):
        """This function is used to add a system log to the status factory."""
        SingletonStatusFactory.add_system_log(system_log)

    def get_service_status(
        self, service: DigitalPyService, config_loader, *args, **kwargs
    ):
        """This function is used to reload the service status of a service."""
        if service is None:
            self.response.set_message("Service not found")
            return

        self.service_status_builder.build_empty_object(config_loader)
        service_status = self.service_status_builder.get_result()
        service_status.service_status = service.status
        service_status.service_name = service.service_id
        if service.process is None:
            service_status.service_status_actual = ServiceStatusEnum.STOPPED
        elif service.process.is_alive():
            service_status.service_status_actual = ServiceStatusEnum.RUNNING
        elif not service.process.is_alive():
            service_status.service_status_actual = ServiceStatusEnum.STOPPED
            service_status.last_error = str(service.process.exitcode)
        service_status.port = service.configuration.port

        SingletonStatusFactory.add_service_status(service_status)
        self.response.set_value("message", service_status)
