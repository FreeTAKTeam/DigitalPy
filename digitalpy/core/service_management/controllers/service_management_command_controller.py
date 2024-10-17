from typing import TYPE_CHECKING

from digitalpy.core.parsing.load_configuration import LoadConfiguration
from digitalpy.core.serialization.configuration.serialization_constants import Protocols

from digitalpy.core.digipy_configuration.domain.builder.action_key_builder import (
    ActionKeyBuilder,
)
from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    CONFIGURATION_PATH_TEMPLATE,
)

from digitalpy.core.zmanager.impl.integration_manager_subscriber import (
    IntegrationManagerSubscriber,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.main.controller import Controller

from digitalpy.core.service_management.digitalpy_service import (
    COMMAND_ACTION,
    COMMAND_PROTOCOL,
)
from digitalpy.core.service_management.domain.model.service_operations import (
    ServiceCommands,
)
from digitalpy.core.service_management.configuration.message_keys import COMMAND
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.domain.model.configuration import (
        Configuration,
    )
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
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
        integration_manager_subscriber: "IntegrationManagerSubscriber",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.integration_manager_pusher = integration_manager_pusher
        self.integration_manager_subscriber = integration_manager_subscriber
        self.action_key_builder = ActionKeyBuilder(
            request, response, sync_action_mapper, configuration
        )

    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        self.action_key_builder.initialize(request, response)

    def send_stop_command(self, service_id: str):
        """Send stop command to the service."""
        command: "Request" = ObjectFactory.get_new_instance("Request")
        command.set_value(COMMAND, ServiceCommands.STOP.value)
        command.action = COMMAND_ACTION
        command.flow_name = self._get_command_flow_name(service_id, command)
        self.integration_manager_pusher.push_container(command)

    def send_get_topics_command(self, service_id: str):
        """Send get topics command to the service."""
        command: "Request" = ObjectFactory.get_new_instance("Request")
        command.set_value(COMMAND, ServiceCommands.GET_TOPICS.value)
        command.action = COMMAND_ACTION
        self._send_command(service_id, command)

    def send_add_topic_command(
        self,
        service_id: str,
        topic: str,
        *args,
        **kwargs,
    ):
        """Send add topic command to the service."""
        command: "Request" = ObjectFactory.get_new_instance("Request")
        command.set_value(COMMAND, ServiceCommands.ADD_TOPIC.value)

        self.action_key_builder.build_empty_object(
            LoadConfiguration(CONFIGURATION_PATH_TEMPLATE)
        )
        self.action_key_builder.add_object_data(topic, Protocols.JSON)
        command.set_value("topic", self.action_key_builder.get_result())

        command.action = COMMAND_ACTION
        self._send_command(service_id, command)

    def send_remove_topic_command(self, service_id: str, topic: str):
        """Send remove topic command to the service."""
        command: "Request" = ObjectFactory.get_new_instance("Request")
        command.set_value(COMMAND, ServiceCommands.REMOVE_TOPIC.value)

        self.action_key_builder.build_empty_object(
            LoadConfiguration(CONFIGURATION_PATH_TEMPLATE)
        )
        self.action_key_builder.add_object_data(topic, Protocols.JSON)
        command.set_value("topic", self.action_key_builder.get_result())

        command.action = COMMAND_ACTION
        self._send_command(service_id, command)

    def _send_command(self, service_id: str, command: "Request"):
        """Send command to the service."""
        command.set_value("prev_flows", [self.request])
        flow_name = self._get_command_flow_name(service_id, command)
        command.flow_name = flow_name
        self.integration_manager_pusher.push_container(command)

    def _get_command_flow_name(self, service_id: str, command: "Request"):
        """Get the name of the command flow given the service_id and commmand.
        This assumes that the service is subscribed to the expected command flow.
        """
        return f"{COMMAND_PROTOCOL}_{service_id}_{command.get_value('command')}"
