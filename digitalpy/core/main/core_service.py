from abc import abstractmethod
from typing import TYPE_CHECKING
import threading
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.impl.subject_pusher import SubjectPusher
from digitalpy.core.zmanager.impl.integration_manager_subscriber import (
    IntegrationManagerSubscriber,
)
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.configuration.zmanager_constants import PUBLISH_DECORATOR
from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    ACTION_MAPPING_SECTION,
)

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.domain.model.configuration import (
        Configuration,
    )
    from digitalpy.core.digipy_configuration.action_key_controller import (
        ActionKeyController,
    )
    from digitalpy.core.serialization.controllers.serializer_container import (
        SerializerContainer,
    )
    from digitalpy.core.component_management.impl.default_facade import DefaultFacade
    from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
        ActionFlowController,
    )


class CoreService(threading.Thread):
    """This is the base class for all threads in the core process.

    It provides the methods required to receive data from the subject and communicate with
    the integration manager.

    It does not expose any form of network only being signaled by the subject or integration
    manager.

    A core service is expected to be a singleton, therefore any repeat call to start or stop
    will raise an exception.
    """

    _default_facade: "DefaultFacade"

    def __init__(
        self,
        service_id: str,
        integration_manager_subscriber: IntegrationManagerSubscriber,
        subject_pusher: SubjectPusher,
    ):
        super().__init__(group=None, target=None, name=service_id, daemon=False)

        self.id: str = service_id

        self.__running: threading.Event = threading.Event()

        self.integration_manager_subscriber = integration_manager_subscriber
        self.integration_manager_subscriber.service_id = self.id

        self.subject_pusher = subject_pusher
        self.subject_pusher.service_id = self.id

        self.action_mapping = {}

        self.action_key_controller: "ActionKeyController" = ObjectFactory.get_instance(
            "ActionKeyController"
        )

        self.action_flow_controller: "ActionFlowController" = (
            ObjectFactory.get_instance("ActionFlowController")
        )

    @property
    def facade(self):
        """Return the default facade."""
        return self._default_facade

    @facade.setter
    def facade(self, facade: "DefaultFacade"):
        """Set the default facade."""
        self._default_facade = facade

    def stop(self):
        """signal the running thread that it is expected to stop operations."""
        self.__running.clear()

    def _teardown(self):
        """release all claimed resources and perform any additional cleanup before shutting down."""
        self.__running.clear()
        self.integration_manager_subscriber.teardown()
        self.subject_pusher.teardown()

    def _setup(self):
        """allocate all necessary resources for runtime."""
        self.__running.set()
        self.integration_manager_subscriber.setup()
        self.subject_pusher.setup()
        self._subscribe_to_actions()
        self._subscribe_to_flow_actions()

    def _subscribe_to_actions(self):
        """subscribe to the actions that the service will be listening to."""
        for entry in self.action_mapping[ACTION_MAPPING_SECTION].items():
            ak = self.action_key_controller.build_from_dictionary_entry(entry)
            ak_res = self.action_key_controller.resolve_action_key(ak)
            ak_res.decorator = PUBLISH_DECORATOR
            self.integration_manager_subscriber.subscribe_to_action(ak_res)

    def _subscribe_to_flow_actions(self):
        """subscribe to the actions within flows that the service will be listening to.
        TODO: This method is inneficient and should be refactored to avoid the nested loop.
        """
        for entry in self.action_mapping[ACTION_MAPPING_SECTION].items():
            ak = self.action_key_controller.build_from_dictionary_entry(entry)
            ak_res = self.action_key_controller.resolve_action_key(ak)
            for action in self.action_flow_controller.get_all_flow_actions(ak_res):
                self.integration_manager_subscriber.subscribe_to_action(action)

    def run(self) -> None:
        """This is the main entry point for the thread. It will start the event loop and
        run until the stop method is called.
        """
        self._setup()
        while self.__running.is_set():
            try:
                self.reactor()
            except Exception as e:  # pylint: disable=broad-except
                self.exception_handler(e)
        self._teardown()

    @abstractmethod
    def reactor(self):
        """This is the central method of the class. It is abstract and should be implemented
        by all subclasses.

        This should contain the central flow of how a given request should be handled.
        """

    def exception_handler(self, e: Exception):
        """This method will handle any exceptions that occur during the reactor method."""
        self._teardown()
        raise RuntimeError(
            "An unhandled exception occured during the execution of the service "
            + self.__class__.__name__
        ) from e

    def _send_next_action(self, request: Request, response: Response):
        """Send the next action to the subject."""
        # Get the next action
        next_action = self.action_flow_controller.get_next_message_action(request)
        # Resolve the action key
        response.action_key = self.action_key_controller.resolve_action_key(next_action)
        # Send the updated response to the subject to handle the next action in the sequence
        self.subject_pusher.push_container(response)

    def _handle_integration_manager_request(self, request: Request):
        """Handle the integration manager request."""
        # Execute the method in the configured facade
        response: Response = ObjectFactory.get_new_instance("Response")
        self.facade.initialize(request, response)
        self.facade.execute(request.action)

        # Send subsequent actions to the subject
        next_action = self.action_flow_controller.get_next_message_action(request)
        if next_action:
            response.action_key = next_action
            response.id = request.id
            self.subject_pusher.push_container(response)
        else:
            self.integration_manager_pusher.push_container(response)
