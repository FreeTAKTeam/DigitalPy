#######################################################
#
# core_name_controller.py
# Python implementation of the Class CoreNameRulesController
# Generated by Enterprise Architect
# Created on:      16-Dec-2022 10:56:02 AM
# Original author: Giu Platania
#
#######################################################


from typing import TYPE_CHECKING, Dict

from digitalpy.core.zmanager.impl.integration_manager_subscriber import (
    IntegrationManagerSubscriber,
)
from digitalpy.core.service_management.controllers.service_management_command_controller import (
    ServiceManagementCommandController,
)
from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.service_management.controllers.service_management_status_controller import (
    ServiceManagementStatusController,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.service_management.domain.model.service_configuration import (
    ServiceConfiguration,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.service_management.controllers.service_management_process_controller import (
    ServiceManagementProcessController,
)
from digitalpy.core.main.controller import Controller

# import builders

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.domain.model.configuration import (
        Configuration,
    )
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient
    from digitalpy.core.component_management.domain.model.component import Component
    from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
    from digitalpy.core.component_management.domain.model.error import Error
    from digitalpy.core.zmanager.impl.integration_manager_pusher import (
        IntegrationManagerPusher,
    )


class ServiceManagementController(Controller):
    """This class is used to manage the services."""

    def __init__(
        self,
        request: "Request",
        response: "Response",
        sync_action_mapper: "DefaultActionMapper",
        configuration: "Configuration",
        integration_manager_pusher: "IntegrationManagerPusher",
        integration_manager_subscriber: "IntegrationManagerSubscriber",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.service_management_process_controller = ServiceManagementProcessController(
            request,
            response,
            sync_action_mapper,
            configuration,
        )
        self.service_management_status_controller = ServiceManagementStatusController(
            request,
            response,
            sync_action_mapper,
            configuration,
        )
        self.service_command_controller = ServiceManagementCommandController(
            request,
            response,
            sync_action_mapper,
            configuration,
            integration_manager_pusher,
            integration_manager_subscriber,
        )
        self._services: Dict[str, DigitalPyService] = {}

    def initialize(self, request: "Request", response: "Response"):
        """This function is used to initialize the controller."""
        super().initialize(request, response)
        self.service_management_process_controller.initialize(request, response)
        self.service_management_status_controller.initialize(request, response)
        self.service_command_controller.initialize(request, response)

    def initialize_service(self, service_id: str, *args, **kwargs):
        """This function is used to initialize the service. It first retrieves the service status
        from the status factory. Based on the status, it either starts the service or does nothing.
        Finally, it adds the service to the service index.

        Args:
            service_id: The ID of the service to initialize
        """
        service_configuration: ServiceConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(service_id)
        )
        # initialize the service based on the service_id
        service = ObjectFactory.get_instance(
            service_id, {"service": service_configuration}
        )
        self._services[service_id] = service
        match ServiceStatusEnum(service_configuration.status):
            case ServiceStatusEnum.RUNNING:
                self.start_service(service_id)
            case _:
                pass

    def start_service(self, service_id: str, *args, **kwargs):
        """This function is used to start the service."""
        service = self._services[service_id]
        self.service_management_process_controller.start_process(service)
        self.response.set_value("message", service.configuration)

    def stop_service(self, service_id: str, *args, **kwargs):
        """This function is used to stop the service."""
        service = self._services[service_id]
        self.service_command_controller.send_stop_command(service.service_id)
        self.service_management_process_controller.stop_process(service)
        self.response.set_value("message", service.configuration)

    def restart_service(self, service_id: str, *args, **kwargs):
        """This function is used to restart the service."""
        self.stop_service(service_id)
        self.start_service(service_id)

    def get_service_status(self, service_id: str, config_loader, *args, **kwargs):
        """This function is used to get the status of the service."""
        service = self._services[service_id]
        self.service_management_status_controller.get_service_status(
            service, config_loader
        )

    def get_service_topics(self, service_id: str, *args, **kwargs):
        """This function is used to get the topics of the service."""
        service = self._services[service_id]
        if service is None:
            raise ValueError("Service not found")
        if service.status == ServiceStatusEnum.RUNNING.value:
            self.service_command_controller.send_get_topics_command(service_id)
        else:
            raise RuntimeError("Service is not running")

    def get_service_topics_response(self, message: str, *args, **kwargs):
        """This function is used to get the topics response of the service, in this case it's functionality is basically arbitrary
        as it's simply ensuring the message is set to the response and that the message is present.
        """
        if message is None:
            raise ValueError("Message not found")
        self.response.set_id(self.request.id)
        self.response.set_value("message", message)

    def put_service_topic(self, service_id: str, topic: str, *args, **kwargs):
        """This function is used to put the topics of the service."""
        service = self._services[service_id]
        if service is None:
            raise ValueError("Service not found")
        if service.status == ServiceStatusEnum.RUNNING.value:
            self.service_command_controller.send_add_topic_command(service_id, topic)
        else:
            raise RuntimeError("Service is not running")

    def put_service_topics_response(self, message: str, *args, **kwargs):
        """This function is used to put the topics response of the service, in this case it's functionality is basically arbitrary
        as it's simply ensuring the message is set to the response and that the message is present.
        """
        if message is None:
            raise ValueError("Message not found")
        self.response.set_id(self.request.id)
        self.response.set_value("message", message)

    def delete_service_topic(self, service_id: str, topic: str, *args, **kwargs):
        """This function is used to delete the topics of the service."""
        service = self._services[service_id]
        if service is None:
            raise ValueError("Service not found")
        if service.status == ServiceStatusEnum.RUNNING.value:
            self.service_command_controller.send_remove_topic_command(service_id, topic)
        else:
            raise RuntimeError("Service is not running")

    def delete_service_topic_response(self, message: str, *args, **kwargs):
        """This function is used to delete the topics response of the service, in this case it's functionality is basically arbitrary
        as it's simply ensuring the message is set to the response and that the message is present.
        """
        if message is None:
            raise ValueError("Message not found")
        self.response.set_id(self.request.id)
        self.response.set_value("message", message)
