from abc import ABC, abstractmethod
from typing import List, Union
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response


class NetworkInterface(ABC):
    """Network  Interface class. Defines the interface for all networking implementations
    """

    @abstractmethod
    def service_connections(self) -> List[Request]:
        """service all connections to the server and return a list of Requests

        Returns:
            List[Request]: _description_
        """

    @abstractmethod
    def intialize_network(self, host: str, port: int, *args, **kwargs):
        """initialize the network connection, bind to the port and host.
        """

    @abstractmethod
    def teardown_network(self):
        """stop listening for messages from the network and release all files and resources
        """

    @abstractmethod
    def receive_message(self, blocking: bool = False) -> Request:
        """receive the next queued message from the network
        Args:
            blocking (bool, optional): whether or not to block until a message is received. Defaults to False.
        Returns:
            Request: the received message
        """

    @abstractmethod
    def send_response(self, response: Response):
        """send a response to the network
        Args:
            response (Response): the response to send
        Raises:
            IOError: if the response cannot be sent
        """
