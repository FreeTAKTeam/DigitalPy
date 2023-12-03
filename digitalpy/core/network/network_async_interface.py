from abc import ABC, abstractmethod
from digitalpy.core.network.domain.network_client import NetworkClient
from digitalpy.core.zmanager.response import Response


class NetworkAsyncInterface(ABC):
    """Network Async Interface class. Defines the interface for implementations of asynchronous networking
    """

    @abstractmethod
    def start_listening(self):
        """start listening for messages from the network, this should be called before any 
        other methods and should be called as a thread.
        """

    @abstractmethod
    def stop_listening(self):
        """stop listening for messages from the network
        """

    @abstractmethod
    def receive_message(self, blocking: bool = False) -> Response:
        """receive the next queued message from the network
        Args:
            blocking (bool, optional): whether or not to block until a message is received. Defaults to False.
        Returns:
            Response: the received message
        """

    @abstractmethod
    def receive_message_from_client(self, client: NetworkClient, blocking: bool = False) -> Response:
        """receive the next queued message from the network from a specific client
        Args:
            client_id (int): the id of the client to receive the message from
            blocking (bool, optional): whether or not to block until a message is received. Defaults to False.
        """

    @abstractmethod
    def send_message_to_client(self, message: Response, client: NetworkClient):
        """send a message to the network
        Args:
            message (Response): the message to send
            client_id (int): the id of the client to send the message to

        Raises:
            ValueError: if the client_id is not valid
            IOError: if the message cannot be sent
        """

    @abstractmethod
    def send_message_to_all_clients(self, message: Response, suppress_failed_sending: bool = False):
        """ send a message to all clients on the network
        Args:
            message (Response): the message to send
            suppress_failed_sending (bool, optional): whether or not to suppress any errors that occur when sending the message to a client. Defaults to False.
        Raises:
            IOError: if the message cannot be sent to one or all clients
        """
