from datetime import datetime as dt
from multiprocessing import Process
from digitalpy.core.domain.node import Node
from digitalpy.core.parsing.load_configuration import ModelConfiguration


class ServiceConfiguration(Node):
    """
    This class defines the basic configuration of a service in a digitalpy environment.
    Attributes:
        protocol (str): The protocol of the service.
        status (str): The status of the service in its lifecycle.
        name (str): The human-readable name of the service.
        host (str): The host address if the process is attached to a network.
        port (int): The port if the process is attached to a network.
    """

    def __init__(
        self,
        model_configuration=ModelConfiguration(),
        model={},
        node_type="service_description",
        oid=None,
    ) -> None:
        super().__init__(
            model_configuration=model_configuration,
            model=model,
            node_type=node_type,
            oid=oid,
        )
        self._protocol: str = None  # type: ignore
        self._status: str = None  # type: ignore
        self._name: str = None  # type: ignore
        self._host: str = None  # type: ignore
        self._port: int = None  # type: ignore

    @property
    def protocol(self) -> str:
        return self._protocol

    @protocol.setter
    def protocol(self, value: str) -> None:
        self._protocol = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str) -> None:
        self._host = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        self._port = value
