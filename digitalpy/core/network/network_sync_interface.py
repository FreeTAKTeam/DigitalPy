from abc import abstractmethod
from typing import List
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.network.network_interface import NetworkInterface
from digitalpy.core.zmanager.request import Request


class NetworkSyncInterface(NetworkInterface):
    """Network Async Interface class. Defines the interface for implementations of asynchronous networking
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
