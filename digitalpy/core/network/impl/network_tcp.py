"""This file defines a class `TCPNetwork` that implements the `NetworkAsyncInterface`. This class is used to establish a network communication using the TCP protocol. It uses the ZeroMQ library for creating the socket and context for communication. 

The class has methods for initializing the network (`intialize_network`) and connecting a client to the server (`connect_client`). The `initialize_network` method sets up the ZeroMQ context and socket, binds it to the provided host and port. The `connect_client` method is used to connect a client to the server using the client's identity. 

The class also maintains a dictionary of clients connected to the network, with their identities as keys.
"""

from typing import Dict, List, TYPE_CHECKING, Union
import zmq
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.network.domain.client_status import ClientStatus
from digitalpy.core.domain.object_id import ObjectId

from digitalpy.core.network.network_async_interface import NetworkAsyncInterface
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

if TYPE_CHECKING:
    from digitalpy.core.domain.domain_facade import Domain


class TCPNetwork(NetworkAsyncInterface):
    """this class implements the NetworkAsyncInterface using the TCP protocol realizing
    the simplified approach to network communication
    """

    def __init__(self):
        self.host: str = None  # type: ignore
        self.port: int = None  # type: ignore
        self.socket: zmq.Socket = None  # type: ignore
        self.context: zmq.Context = None  # type: ignore
        self.clients: Dict[str, NetworkClient] = {}

    def initialize_network(self, host: str, port: int):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.STREAM)
        self.socket.getsockopt_string(zmq.IDENTITY)
        self.socket.bind(f"tcp://{host}:{port}")

    def connect_client(self, identity: bytes) -> NetworkClient:
        """connect a client to the server

        Args:
            identity (bytes): the identity of the client
        """
        client = self.handle_client_connection(identity)

        self.clients[str(client.id)] = client

        return client

    def handle_client_disconnection(self, client: NetworkClient):
        """disconnect a client from the server

        Args:
            identity (NetworkClient): the network client to disconnect
        """
        client.status = ClientStatus.DISCONNECTED

        return self.clients.pop(str(client.id))

    def handle_empty_msg(self, identity: bytes, request: Request) -> NetworkClient:
        """handle an empty message from the client

        Args:
            client (NetworkClient): the client that sent the empty message
        """
        client = self.clients.get(str(identity))
        if not client:
            request.set_value("action", "connection")
            return self.connect_client(identity)
        else:
            request.set_value("action", "disconnection")
            return self.handle_client_disconnection(client)

    def service_connections(
        self, max_requests=1000, blocking: bool = False, timeout: int = 0
    ) -> List[Request]:
        """service all connections to the server and return a list of requests

        Args:
            max_requests (int, optional): the maximum number of requests to service. Defaults to 1000.
            blocking (bool, optional): whether or not to block until a request is received. Defaults to False.
            timeout (int, optional): the number of seconds to wait for a request before returning. Defaults to 0.

        Returns:
            List[request]: a list of requests from the clients
        """
        requests = []
        try:
            # wait for first message
            req = self.service_connection(blocking=blocking, timeout=timeout)
            requests.append(req)
            # receive messages until the max_requests is reached or there are no more messages
            while len(requests) < max_requests:
                req = self.service_connection(blocking=False)
                requests.append(req)

        # receive messages should throw an exception when there are no messages to receive
        except zmq.Again:
            pass

        return requests

    def service_connection(self, blocking: bool = False, timeout: int = 0) -> Request:
        """service a single connection to the server and return a request

        Args:
            blocking (bool, optional): whether or not to block until a request is received. Defaults to False.
            timeout (int, optional): the number of seconds to wait for a request before returning. Defaults to 0.

        Returns:
            Request: a request from the client

        Raises:
            zmq.Again: if there are no messages to receive
        """
        # receive the identity of the client and it's message contents
        identity = self.receive_message(blocking=blocking, timeout=timeout)
        msg = self.receive_message(blocking=False)

        # construct a request
        req: Request = ObjectFactory.get_new_instance("Request")
        req.set_value("data", msg)

        if msg == b"":
            client = self.handle_empty_msg(identity, req)

        else:
            client = self.clients.get(str(identity))

        req.set_value("client", client)

        return req

    def teardown_network(self):
        if self.socket:
            self.socket.close()

    def receive_message(self, blocking: bool = False, timeout: int = 0) -> bytes:
        # Implement logic to receive a message from any client
        if not blocking:
            msg = self.socket.recv(zmq.NOBLOCK)
        else:
            self.socket.setsockopt(zmq.RCVTIMEO, timeout)
            msg = self.socket.recv()
        return msg

    def handle_client_connection(self, network_id: bytes) -> NetworkClient:
        """handle a client connection"""
        oid = ObjectId("network_client", id=str(network_id))
        client: NetworkClient = ObjectFactory.get_new_instance(
            "DefaultClient", dynamic_configuration={"oid": oid}
        )
        client.id = network_id
        client.status = ClientStatus.CONNECTED
        return client

    def receive_message_from_client(
        self, client: NetworkClient, blocking: bool = False
    ) -> Request:
        # Implement logic to receive a message from a specific client
        return None  # type: ignore

    def send_response(self, response: Response):
        if response.get_value("client") is None or response.get_value("client") == "*":
            self.send_message_to_all_clients(response)
        else:
            self.send_message_to_clients(response, response.get_value("client"))

    def send_message_to_client(self, message: Response, client: NetworkClient):
        try:
            for message_data in message.get_value("message"):
                self.socket.send_multipart([client.id, message_data])
        except Exception as e:
            raise IOError(f"Failed to send message to client {client}: {str(e)}") from e

    def send_message_to_clients(
        self, message: Response, clients: Union[List[NetworkClient], List[str]]
    ):
        for client in clients:
            if isinstance(client, str):
                oid = ObjectId.parse(client)
                if oid is None:
                    raise ValueError(f"Invalid client id: {client}")
                client = self.clients.get(oid.get_id()[0])
                if client is None:
                    raise ValueError(f"Client not found: {client}")
            self.send_message_to_client(message, client)

    def send_message_to_all_clients(
        self, message: Response, suppress_failed_sending: bool = False
    ):
        for client in self.clients.values():
            try:
                self.send_message_to_client(message, client)
            except IOError as e:
                if not suppress_failed_sending:
                    raise IOError(
                        f"Failed to send message to client {client}: {str(e)}"
                    )
