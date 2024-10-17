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
    from digitalpy.core.zmanager.controller_message import ControllerMessage


class Pusher(ABC):
    def __init__(self, formatter: "Formatter", pull_address: str) -> None:
        # list of connection to which the socket should reconnect after
        # being unpickled
        self.__pusher_socket_connections: list[tuple[bool, str]] = []
        self.pusher_context: zmq.Context = None  # type: ignore
        self.pusher_socket: zmq.Socket = None  # type: ignore
        self.pusher_formatter: Formatter = formatter
        self.pull_address = pull_address
        self.serializer_container: "SerializerContainer" = ObjectFactory.get_instance(
            "SerializerContainer"
        )

    def setup(self, bind: bool = False) -> None:
        """initiate subject connection

        Args:
            bind (bool): if the connection should bind to the address
        """
        # added to fix hanging connect issue as per
        # https://stackoverflow.com/questions/44257579/zeromq-hangs-in-a-python-multiprocessing-class-object-solution
        if self.pusher_context is None:
            self.pusher_context = zmq.Context()
        if self.pusher_socket is None:
            self.pusher_socket = self.pusher_context.socket(zmq.PUSH)
        if bind:
            self.pusher_socket.bind(self.pull_address)
        else:
            self.pusher_socket.connect(self.pull_address)
        self.__pusher_socket_connections.append((bind, self.pull_address))

    def teardown(self):
        """teardown subject connection"""
        for connection in self.__pusher_socket_connections:
            if connection[0]:
                self.pusher_socket.unbind(connection[1])
            else:
                self.pusher_socket.disconnect(connection[1])
        self.pusher_socket.close()
        self.pusher_context.term()
        self.pusher_context.destroy()
        self.pusher_socket = None  # type: ignore
        self.pusher_context = None  # type: ignore

    def push_container(self, container: "ControllerMessage"):  # type: ignore
        """send the container object to the target

        Args:
            container (ControllerMessage): the request to be sent to the target
        """
        # set the service_id so it can be used to create the publish topic by the default routing worker
        message = self.serializer_container.to_zmanager_message(container)
        if len(self.__pusher_socket_connections) > 0:
            self.pusher_socket.send(message)
        else:
            raise ConnectionError("No connection to pusher established")

    def __getstate__(self):
        state = self.__dict__
        if "pusher_socket" in state:
            state["pusher_socket"] = None
        if "pusher_context" in state:
            state["pusher_context"] = None
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        if self.pusher_context is None:
            self.pusher_context = zmq.Context()
        if self.pusher_socket is None:
            self.pusher_socket = self.pusher_context.socket(zmq.PUSH)

            for connection in self.__pusher_socket_connections:
                if connection[0]:
                    self.pusher_socket.bind(connection[1])
                else:
                    self.pusher_socket.connect(connection[1])
