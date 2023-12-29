from digitalpy.core.domain.node import Node
from digitalpy.core.parsing.load_configuration import ModelConfiguration

from .client_status import ClientStatus


class NetworkClient(Node):
    """this class represents a network client in the digitalpy framework,
        it is the base network client implementation and can be expanded"""

    def __init__(self, configuration=None, model=None, oid=None, node_type="network_client") -> None:
        super().__init__(node_type, configuration=configuration,
                         model=model, oid=oid)  # type: ignore
        # the id of the client
        self._id: bytes
        # the status of the client
        self._status: ClientStatus = ClientStatus.CONNECTING
        # id of the related service
        self._service_id: str
        # the protocol used by the client
        self._protocol: str

    @property
    def protocol(self) -> str:
        """get the protocol of the client

        Returns:
            str: the protocol of the client
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: str):
        """set the protocol of the client

        Args:
            protocol (str): the protocol of the client
        """
        if not isinstance(protocol, str):
            raise TypeError("'protocol' must be an instance of str")
        self._protocol = protocol

    @property
    def service_id(self) -> str:
        """get the service id of the client

        Returns:
            str: the service id of the client
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id: str):
        """set the service id of the client

        Args:
            service_id (str): the service id of the client
        """
        if not isinstance(service_id, str):
            raise TypeError("'service_id' must be an instance of str")
        self._service_id = service_id

    @property
    def status(self) -> ClientStatus:
        """get the status of the client

        Returns:
            str: the status of the client
        """
        return self._status

    @status.setter
    def status(self, status: ClientStatus):
        """set the status of the client

        Args:
            status (str): the status of the client
        """
        if status not in ClientStatus:
            raise ValueError("'status' must be a valid ClientStatus")
        self._status = status

    @property
    def id(self) -> bytes:
        """get the id of the client

        Returns:
            bytes: the id of the client
        """
        return self._id

    @id.setter
    def id(self, id: bytes):
        """set the id of the client

        Args:
            id (bytes): the id of the client
        """
        if not isinstance(id, bytes):
            raise TypeError("'id' must be an instance of int")
        self._id = id
