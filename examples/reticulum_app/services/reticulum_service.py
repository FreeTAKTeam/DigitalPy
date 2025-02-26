import importlib
import pathlib
import traceback
import os

from digitalpy.core.serialization.serialization_facade import Serialization
from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.zmanager.impl.integration_manager_subscriber import (
    IntegrationManagerSubscriber,
)
from digitalpy.core.zmanager.impl.integration_manager_pusher import (
    IntegrationManagerPusher,
)
from digitalpy.core.zmanager.impl.subject_pusher import SubjectPusher
from digitalpy.core.service_management.domain.model.service_configuration import (
    ServiceConfiguration,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.digitalpy_service import (
    DigitalPyService,
    COMMAND_ACTION,
)
from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.zmanager.response import Response


CONFIGURATION_SECTION = "reticulum_app.reticulum"


class ReticulumService(DigitalPyService):
    def __init__(
        self,
        service: ServiceConfiguration,
        integration_manager_subscriber: IntegrationManagerSubscriber,
        integration_manager_pusher: IntegrationManagerPusher,
        subject_pusher: SubjectPusher,
        identity_path: str,
        storage_path: str,
    ):
        super().__init__(
            service_id="reticulum_app.reticulum",
            service=service,
            integration_manager_subscriber=integration_manager_subscriber,
            subject_pusher=subject_pusher,
            integration_manager_pusher=integration_manager_pusher,
        )
        self._identity_path = identity_path
        self._storage_path = storage_path

    def handle_inbound_message(self, message):
        self.handle_ret_message(message)

    def handle_ret_message(self, message: Request):
        message.set_format("pickled")
        flow =SingletonConfigurationFactory.get_action_flow("ChatMessageFlow")
        message.action_key = flow.actions[0]
        self._subject_pusher.push_container(message)

    def serialize(self, message):
        return message.get_value("message")

    def handle_response(self, response: Response):
        self.serialize(response)
        self.protocol.send_response(response)

    def start(self, object_factory: DefaultFactory, tracing_provider: TracingProvider, conf_factory: ConfigurationFactory):
        SingletonConfigurationFactory().configure(conf_factory)
        ObjectFactory().configure(object_factory)
        self.tracer = tracing_provider.create_tracer(self.service_id)
        self.initialize_controllers()
        self.initialize_connections()

        self.protocol.initialize_network(
            None,
            None,
            self._identity_path,
            self._storage_path,
            self.configuration,
        )
        self.status = ServiceStatusEnum.RUNNING.value
        self.execute_main_loop()


        