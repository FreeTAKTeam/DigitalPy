"""Service Management Core module."""

from typing import TYPE_CHECKING, Dict

from digitalpy.core.service_management.digitalpy_service import COMPLETED_COMMAND

from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.zmanager.impl.integration_manager_pusher import (
    IntegrationManagerPusher,
)
from digitalpy.core.main.singleton_status_factory import SingletonStatusFactory
from digitalpy.core.main.impl.status_factory import StatusFactory
from digitalpy.core.service_management.domain.model.service_description import (
    ServiceDescription,
)
from digitalpy.core.service_management.domain.model.service_management_configuration import (
    ServiceManagementConfiguration,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)

from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.impl.subject_pusher import SubjectPusher
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.impl.integration_manager_subscriber import (
    IntegrationManagerSubscriber,
)
from digitalpy.core.main.core_service import CoreService
from digitalpy.core.service_management.service_management_facade import (
    ServiceManagement,
)

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.action_key_controller import (
        ActionKeyController,
    )


class ServiceManagementCore(CoreService):
    """Service Management Core class."""

    def __init__(
        self,
        integration_manager_subscriber: IntegrationManagerSubscriber,
        subject_pusher: SubjectPusher,
        status_factory: StatusFactory,
        integration_manager_pusher: IntegrationManagerPusher,
    ):
        super().__init__(
            service_id="service_management_core",
            integration_manager_subscriber=integration_manager_subscriber,
            subject_pusher=subject_pusher,
            integration_manager_pusher=integration_manager_pusher,
        )

        # integration_manager_pusher.setup()

        SingletonStatusFactory.configure(status_factory)

        self.service_management_facade: ServiceManagement = ObjectFactory.get_instance(
            "ServiceManagement",
            dynamic_configuration={
                "integration_manager_pusher": integration_manager_pusher
            },
        )

        self.action_key_controller: "ActionKeyController" = ObjectFactory.get_instance(
            "ActionKeyController"
        )

        self.service_management_configuration: ServiceManagementConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ServiceManagementConfiguration"
            )
        )

        self._service_index: Dict[str, ServiceDescription] = {}

        self.action_mapper: ActionMapper = ObjectFactory.get_instance(
            "SyncActionMapper"
        )

        # set the action mapping so that the service is subscribed to the integration manager properly
        self.action_mapping = self.service_management_facade.get_action_mapping()

        # set the flow path for the service
        self.flow_path = self.service_management_facade.get_flow_configuration_path()

        # set the facade to the service management facade
        self.facade = self.service_management_facade

    def _setup(self):
        super()._setup()
        self._subscribe_to_commands()
        self.initialize_all_services()

    def _subscribe_to_commands(self):
        """subscribe to the commands that the service will be listening to."""
        command_action: ActionKey = ActionKey(None, None)
        command_action.config = COMPLETED_COMMAND
        self.integration_manager_subscriber.subscribe_to_action(command_action)

    def initialize_all_services(self):
        """Initialize all services to their default state."""
        services = self.service_management_configuration.services
        for service_section in services:
            self.initialize_service(service_section)

    def initialize_service(self, service_class: str):
        """Initialize a service to its default state."""
        self.service_management_facade.initialize_service(service_class)

    def reactor(self):
        """the main loop of the service management core which responds to events and is
        non-blocking."""
        request = (
            self.integration_manager_subscriber.fetch_integration_manager_request()
        )
        if request:
            self._handle_integration_manager_request(request)

    def _handle_completed_flow(self, response: Response):
        """Handle a completed flow."""
        if response.get_value("prev_flows"):
            prev_req: Request = response.get_value("prev_flows")[0]
            next_act = self.action_flow_controller.get_next_action(prev_req.action_key)
            response.set_action_key(next_act)
            response.set_id(prev_req.get_id())
        return response

    def _handle_integration_manager_request(self, request: Request):
        """Handle the integration manager request."""
        if request.action == "done":
            request = self._handle_completed_flow(request)
        super()._handle_integration_manager_request(request)
