from digitalpy.core.domain.node import Node

from .client_status import ClientStatus

class NetworkClient(Node):
    def __init__(self, node_type="network_client", oid=None) -> None:
        super().__init__(node_type, oid=oid)
        # the id of the client
        self._id: int = 0
        # the status of the client
        self._status: str = ClientStatus.CONNECTING

    @property
    def status(self) -> str:
        """get the status of the client

        Returns:
            str: the status of the client
        """
        return self._status
    
    @status.setter
    def status(self, status: str):
        """set the status of the client

        Args:
            status (str): the status of the client
        """
        if status not in ClientStatus:
            raise ValueError("'status' must be a valid ClientStatus")
        self._status = status

    @property
    def id(self) -> int:
        """get the id of the client

        Returns:
            int: the id of the client
        """
        return self._id
    
    @id.setter
    def id(self, id: int):
        """set the id of the client

        Args:
            id (int): the id of the client
        """
        if not isinstance(id, int):
            raise TypeError("'id' must be an instance of int")
        if id < 0:
            raise ValueError("'id' must be greater than or equal to 0")
        if self._id != None:
            raise ValueError("'id' cannot be changed once set")
        self._id = id