from abc import abstractmethod
from typing import List
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.network.network_interface import NetworkInterface
from digitalpy.core.zmanager.request import Request


class NetworkAsyncInterface(NetworkInterface):
    """Network Async Interface class. Defines the interface for implementations of asynchronous networking
    """

    @abstractmethod
    def service_connections(self) -> List[Request]:
        """service all connections to the server and return a list of Requests

        Returns:
            List[Request]: _description_
        """

    @abstractmethod
    def intialize_network(self, host: str, port: int):
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
    def receive_message_from_client(self, client: NetworkClient, blocking: bool = False) -> Request:
        """receive the next queued message from the network from a specific client
        Args:
            client_id (int): the id of the client to receive the message from
            blocking (bool, optional): whether or not to block until a message is received. Defaults to False.
        """

    @abstractmethod
    def send_message_to_client(self, message: Request, client: NetworkClient):
        """send a message to the network
        Args:
            message (Request): the message to send
            client_id (int): the id of the client to send the message to

        Raises:
            ValueError: if the client_id is not valid
            IOError: if the message cannot be sent
        """

    @abstractmethod
    def send_message_to_all_clients(self, message: Request, suppress_failed_sending: bool = False):
        """ send a message to all clients on the network
        Args:
            message (Request): the message to send
            suppress_failed_sending (bool, optional): whether or not to suppress any errors that occur when sending the message to a client. Defaults to False.
        Raises:
            IOError: if the message cannot be sent to one or all clients
        """
