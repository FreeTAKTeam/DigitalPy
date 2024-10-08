from abc import ABC
from typing import TYPE_CHECKING
import zmq

from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.main.object_factory import ObjectFactory

if TYPE_CHECKING:
    from digitalpy.core.serialization.controllers.serializer_container import (
        SerializerContainer,
    )
    from digitalpy.core.zmanager.domain.model.zmanager_configuration import (
        ZManagerConfiguration,
    )
    from digitalpy.core.parsing.formatter import Formatter


class Pusher(ABC):
    def __init__(self, formatter: "Formatter", pull_address: str) -> None:
        # list of connection to which the socket should reconnect after
        # being unpickled
        self.__pusher_socket_connections = []
        self.pusher_context: zmq.Context = None  # type: ignore
        self.pusher_socket: zmq.Socket = None  # type: ignore
        self.pusher_formatter: Formatter = formatter
        self.pull_address = pull_address
        self.serializer_container: "SerializerContainer" = ObjectFactory.get_instance(
            "SerializerContainer"
        )

    def setup(self) -> None:
        """initiate subject connection"""
        # added to fix hanging connect issue as per
        # https://stackoverflow.com/questions/44257579/zeromq-hangs-in-a-python-multiprocessing-class-object-solution
        if self.pusher_context is None:
            self.pusher_context = zmq.Context()
        if self.pusher_socket is None:
            self.pusher_socket = self.pusher_context.socket(zmq.PUSH)
        self.pusher_socket.connect(self.pull_address)
        self.__pusher_socket_connections.append(self.pull_address)

    def teardown(self):
        """teardown subject connection"""
        for connection in self.__pusher_socket_connections:
            self.pusher_socket.disconnect(connection)
        self.pusher_socket.close()
        self.pusher_context.term()
        self.pusher_context.destroy()
        self.pusher_socket = None  # type: ignore
        self.pusher_context = None  # type: ignore

    def push_container(self, container: "ControllerMessage"):  # type: ignore
        """send the container object to the target

        Args:
            container (ControllerMessage): the request to be sent to the subject
            protocol (str): the protocol of the request to be sent
            service_id (str, optional): the service_id of the request to be sent. Defaults to the id of the current service.
        """
        # set the service_id so it can be used to create the publish topic by the default routing worker
        message = self.serializer_container.to_zmanager_message(container)
        self.pusher_socket.send(message)

    def __getstate__(self):
        state = self.__dict__
        if "pusher_socket" in state:
            del state["pusher_socket"]
        if "pusher_context" in state:
            del state["pusher_context"]
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.pusher_context = zmq.Context()
        self.pusher_socket = self.pusher_context.socket(zmq.PUSH)

        for connection in self.__pusher_socket_connections:
            self.pusher_socket.connect(connection)
