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

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.domain.model.configuration import (
        Configuration,
    )
    from digitalpy.core.digipy_configuration.action_key_controller import (
        ActionKeyController,
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

    def _subscribe_to_actions(self):
        """subscribe to the actions that the service will be listening to."""
        for entry in self.action_mapping.items():
            ak = self.action_key_controller.build_from_dictionary_entry(entry)
            ak.decorator = PUBLISH_DECORATOR
            self.integration_manager_subscriber.subscribe_to_action(ak)

    def _send_request(self, request: Request):
        """send a request to the subject."""
        self.subject_pusher.subject_send_request(request, self.id)

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

    def send_response(self, response: Response):
        """This operation will send a response to the integration manager.
        The response will be converted to a message and sent to the integration manager.
        """
