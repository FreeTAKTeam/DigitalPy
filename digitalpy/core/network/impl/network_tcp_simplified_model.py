from typing import List
import zmq
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.network.domain.client_status import ClientStatus

from digitalpy.core.network.network_async_interface import NetworkAsyncInterface
from digitalpy.core.network.domain.network_client import NetworkClient
from digitalpy.core.zmanager.response import Response

class NetworkTCPSimplifiedModel(NetworkAsyncInterface):
    """this class implements the NetworkAsyncInterface using the TCP protocol realizing
    the simplified approach to network communication
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = None
        self.clients = {}

    def service_connections(self) -> List[Response]:
        """service all connections to the server and return a list of responses

        Returns:
            List[Response]: _description_
        """
        responses = []
        msg = self.receive_message()

        while msg != None:
            if msg == b'':
                self.disconnect_client(client)

            identity, _, data = msg
            client = self.clients.get(identity.decode(), None)

            if not client:
                client = self.initialize_new_client(identity)

            resp: Response = ObjectFactory.get_new_instance("Response")
            resp.set_value("data", data)
            resp.set_value("client", client)
            responses.append(resp)
            
            msg = self.receive_message()
        return responses

    def start_listening(self):
        self.socket = self.context.socket(zmq.STREAM)
        self.socket.bind(f"tcp://{self.host}:{self.port}")

    def stop_listening(self):
        if self.socket:
            self.socket.close()

    def receive_message(self, blocking: bool = False) -> Response:
        # Implement logic to receive a message from any client
        if not blocking:
            try:
                msg = self.socket.recv(zmq.NOBLOCK)
            except zmq.Again:
                return None
        else:
            msg = self.socket.recv()
        return msg

    def disconnect_client(self, client: NetworkClient):
        """disconnect the provided client

        Args:
            client (NetworkClient): client to disconnect
        """
        client.status = ClientStatus.DISCONNECTED
        self.clients.pop(client.id)
        return

    def initialize_new_client(self, identity) -> NetworkClient:
        client = NetworkClient()
        client.id = identity
        client.status = ClientStatus.CONNECTED
        self.clients[identity.decode()] = client
        return client

    def receive_message_from_client(self, client: NetworkClient, blocking: bool = False) -> Response:
        # Implement logic to receive a message from a specific client
        pass

    def send_message_to_client(self, message: Response, client: NetworkClient):
        try:
            self.socket.send_multipart([client.identity, b'', message.serialize()])
        except Exception as e:
            raise IOError(f"Failed to send message to client {client}: {str(e)}")

    def send_message_to_all_clients(self, message: Response, suppress_failed_sending: bool = False):
        for client in self.clients.values():
            try:
                self.send_message_to_client(message, client)
            except IOError as e:
                if not suppress_failed_sending:
                    raise IOError(f"Failed to send message to client {client}: {str(e)}")
