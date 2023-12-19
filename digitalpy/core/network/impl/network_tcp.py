"""This file defines a class `TCPNetwork` that implements the `NetworkAsyncInterface`. This class is used to establish a network communication using the TCP protocol. It uses the ZeroMQ library for creating the socket and context for communication. 

The class has methods for initializing the network (`intialize_network`) and connecting a client to the server (`connect_client`). The `initialize_network` method sets up the ZeroMQ context and socket, binds it to the provided host and port. The `connect_client` method is used to connect a client to the server using the client's identity. 

The class also maintains a dictionary of clients connected to the network, with their identities as keys.
"""

from typing import Dict, List
import zmq
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.network.domain.client_status import ClientStatus

from digitalpy.core.network.network_async_interface import NetworkAsyncInterface
from digitalpy.core.network.domain.network_client import NetworkClient
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response


class TCPNetwork(NetworkAsyncInterface):
    """this class implements the NetworkAsyncInterface using the TCP protocol realizing
    the simplified approach to network communication
    """

    def __init__(self):
        self.host: str = None  # type: ignore
        self.port: int = None  # type: ignore
        self.socket: zmq.Socket = None  # type: ignore
        self.context: zmq.Context = None  # type: ignore
        self.clients: Dict[bytes, NetworkClient] = {}

    # TODO: introduce the implementation for client_factory
    def intialize_network(self, host: str, port: int):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.STREAM)
        self.socket.getsockopt_string(zmq.IDENTITY)
        self.socket.bind(f"tcp://{host}:{port}")

    def connect_client(self, identity: bytes) -> NetworkClient:
        """connect a client to the server

        Args:
            identity (bytes): the identity of the client
        """
        client = self.initialize_new_client(identity)

        self.clients[identity] = client

        return client

    def disconnect_client(self, client: NetworkClient):
        """disconnect a client from the server

        Args:
            identity (NetworkClient): the network client to disconnect
        """
        client.status = ClientStatus.DISCONNECTED

        return self.clients.pop(client.id)

    def handle_empty_msg(self, identity: bytes) -> NetworkClient:
        """handle an empty message from the client

        Args:
            client (NetworkClient): the client that sent the empty message
        """
        client = self.clients.get(identity)
        if not client:
            return self.connect_client(identity)
        else:
            return self.disconnect_client(client)

    def service_connections(self, max_requests=1000) -> List[Request]:
        """service all connections to the server and return a list of requests

        Returns:
            List[request]: a list of requests from the clients
        """
        requests = []
        try:

            # avoid blocking indefinitely
            while len(requests) < max_requests:

                # receive the identity of the client and it's message contents
                identity = self.receive_message()
                msg = self.receive_message()

                if msg == b'':
                    client = self.handle_empty_msg(identity)

                else:
                    client = self.clients.get(identity)

                # construct a request and add it to the list of requests
                resp: Request = ObjectFactory.get_new_instance("Request")
                resp.set_value("data", msg)
                resp.set_value("client", client)
                requests.append(resp)

        # receive messages should throw an exception when there are no messages to receive
        except zmq.Again:
            pass

        return requests

    def teardown_network(self):
        if self.socket:
            self.socket.close()

    def receive_message(self, blocking: bool = False) -> bytes:
        # Implement logic to receive a message from any client
        if not blocking:
            msg = self.socket.recv(zmq.NOBLOCK)
        else:
            msg = self.socket.recv()
        return msg

    def initialize_new_client(self, identity) -> NetworkClient:
        client = NetworkClient()
        client.id = identity
        client.status = ClientStatus.CONNECTED
        return client

    def receive_message_from_client(self, client: NetworkClient, blocking: bool = False) -> Request:
        # Implement logic to receive a message from a specific client
        return None # type: ignore

    def send_message_to_client(self, message: Response, client: NetworkClient):
        try:
            self.socket.send_multipart([client.id, b'', message.get_value("data")])
        except Exception as e:
            raise IOError(
                f"Failed to send message to client {client}: {str(e)}")

    def send_message_to_all_clients(self, message: Response, suppress_failed_sending: bool = False):
        for client in self.clients.values():
            try:
                self.send_message_to_client(message, client)
            except IOError as e:
                if not suppress_failed_sending:
                    raise IOError(
                        f"Failed to send message to client {client}: {str(e)}")
