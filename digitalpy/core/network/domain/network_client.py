from digitalpy.core.domain.node import Node

from .client_status import ClientStatus

class NetworkClient(Node):
    def __init__(self, node_type="network_client", oid=None) -> None:
        super().__init__(node_type, oid=oid)
        # the id of the client
        self._id: bytes
        # the status of the client
        self._status: ClientStatus = ClientStatus.CONNECTING

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