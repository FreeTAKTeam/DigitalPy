"""Service Management Core module."""

from typing import TYPE_CHECKING, Dict

from digitalpy.core.service_management.domain.service_description import ServiceDescription
from digitalpy.core.service_management.domain.service_management_configuration import (
    ServiceManagementConfiguration,
)
from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
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
    ):
        super().__init__(
            service_id="service_management_core",
            integration_manager_subscriber=integration_manager_subscriber,
            subject_pusher=subject_pusher,
        )

        self.service_management_facade: ServiceManagement = ObjectFactory.get_instance(
            "ServiceManagement"
        )

        self.action_key_controller: "ActionKeyController" = ObjectFactory.get_instance(
            "ActionKeyController"
        )

        self.service_management_configuration: ServiceManagementConfiguration = (
            SingletonConfigurationFactory.get_configuration_object("ServiceManagementConfiguration")
        )

        self._service_index: Dict[str, ServiceDescription] = {}

    def _setup(self):
        super()._setup()
        self.initialize_all_services()

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

    def _handle_subject_request(self, request: Request):
        """Handle the subject request."""

    def _handle_integration_manager_request(self, request: Request):
        """Handle the integration manager request."""
        response: Response = ObjectFactory.get_new_instance("Response")
        self.service_management_facade.initialize(request, response)
        self.service_management_facade.execute(request.action)
