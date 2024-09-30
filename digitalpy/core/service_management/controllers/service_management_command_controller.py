from typing import TYPE_CHECKING

from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.main.controller import Controller

from digitalpy.core.service_management.digitalpy_service import COMMAND_ACTION
from digitalpy.core.service_management.domain.model.service_operations import (
    ServiceOperations,
)

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


class ServiceManagementCommandController(Controller):
    def __init__(
        self,
        request: "Request",
        response: "Response",
        sync_action_mapper: "DefaultActionMapper",
        configuration: "Configuration",
        integration_manager_pusher: "IntegrationManagerPusher",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.integration_manager_pusher = integration_manager_pusher

    def send_stop_command(self, service_id: str):
        """Send stop command to the service."""
        command: "Request" = ObjectFactory.get_new_instance("Request")
        command.set_value("command", ServiceOperations.STOP.value)
        command.action = COMMAND_ACTION
        command.flow_name = service_id
        self.integration_manager_pusher.push_container(command)
