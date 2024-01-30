"""This file defines a class `TCPNetwork` that implements the `NetworkAsyncInterface`. This class is used to establish a network communication using the TCP protocol. It uses the ZeroMQ library for creating the socket and context for communication. 

The class has methods for initializing the network (`intialize_network`) and connecting a client to the server (`connect_client`). The `initialize_network` method sets up the ZeroMQ context and socket, binds it to the provided host and port. The `connect_client` method is used to connect a client to the server using the client's identity. 

The class also maintains a dictionary of clients connected to the network, with their identities as keys.
"""
import threading
from typing import Dict, List, TYPE_CHECKING, Union
import uuid
from flask import Flask, request as flask_request, session
import pickle

from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.network.domain.client_status import ClientStatus
from digitalpy.core.domain.object_id import ObjectId

from digitalpy.core.network.network_sync_interface import NetworkSyncInterface
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

import zmq

if TYPE_CHECKING:
    from digitalpy.core.domain.domain_facade import Domain


class FlaskHTTPNetwork(NetworkSyncInterface):
    """this class implements the NetworkAsyncInterface using the TCP protocol realizing
    the simplified approach to network communication
    """

    def __init__(self):
        self.host: str = None  # type: ignore
        self.port: int = None  # type: ignore
        self.app: Flask = None  # type: ignore
        self.app_proc: threading.Thread = None  # type: ignore
        self.clients: Dict[int, NetworkClient] = {}
        self.local_context: zmq.Context
        self.sink: zmq.Socket
        self.publisher: zmq.Socket
        self.push_sockets: Dict[str, zmq.Socket] = {}
        self.sub_sockets: Dict[str, zmq.Socket] = {}
        
    def intialize_network(self, host: str, port: int, available_endpoints: List[str] = []):
        self.app = Flask(f"{host}:{port}")
        self.app.secret_key = str(uuid.uuid4())
        self.host = host
        self.port = port
        self.local_context = zmq.Context()
        self.sink = self.local_context.socket(zmq.PULL)
        self.publisher = self.local_context.socket(zmq.PUB)
        self.sink.bind_to_random_port(f"tcp://127.0.0.1")
        self.sink_addr = self.sink.getsockopt(zmq.LAST_ENDPOINT)
        self.publisher.bind_to_random_port(f"tcp://127.0.0.1")
        self.publisher_addr = self.publisher.getsockopt(zmq.LAST_ENDPOINT)

        for endpoint in available_endpoints:
            self.app.add_url_rule(rule = "/"+endpoint, endpoint=endpoint, view_func=self.handle_request)
        self.app_thread = threading.Thread(target=self._start_app, daemon=True)
        self.app_thread.start()

    def _start_app(self):
        self.app.run()
    
    def service_connections(self, max_requests = 1000):
        requests = []
        for _ in range(max_requests):
            try:
                msg = self.receive_message(blocking=False)
                requests.append(msg)
            except zmq.Again:
                return requests
        return requests
    
    def teardown_network(self):
        return super().teardown_network()

    def receive_message(self, blocking: bool = False) -> Request:
        if blocking:
            return self.sink.recv_pyobj()
        else:
            return self.sink.recv_pyobj(zmq.NOBLOCK)

    def receive_message_from_client(self, client: NetworkClient, blocking: bool = False) -> Request:
        return super().receive_message_from_client(client, blocking)

    def handle_connection(self, request: Request, network_id: bytes):
        request.set_value("action", "connection")
        oid = ObjectId("network_client", id=str(network_id))
        client: NetworkClient = ObjectFactory.get_new_instance(
            "DefaultClient", dynamic_configuration={"oid": oid})
        client.id = bytes(network_id)
        client.status = ClientStatus.CONNECTED
        self.clients[network_id] = client

        return client

    def handle_request(self):
        req: Request = ObjectFactory.get_new_instance("Request")
        req.set_value("data", flask_request.get_data())
        client = self._get_client(self._get_id(), req)
        req.set_value("client", client)
        for key, value in flask_request.args.items():
            req.set_value(key, value)
        
        resp: Response = self._forward_request(req)
        return resp.get_value("message")

    def send_response(self, response: Response):
        self.publisher.send_multipart(
                [self._get_message_topic(message=response), pickle.dumps(response)])

    def _forward_request(self, request: Request) -> Response:
        p_s = self._get_push_socket()
        p_s.send_pyobj(request)
        s_s = self._get_sub_socket()
        s_s.subscribe(self._get_message_topic(request))
        resp_raw = s_s.recv_multipart()
        resp = pickle.loads(resp_raw[1])
        s_s.unsubscribe(self._get_message_topic(request))
        return resp
    
    def _get_push_socket(self) -> zmq.Socket:
        thread_id = threading.get_native_id()

        if thread_id not in self.push_sockets:
            sock: zmq.Socket = self.local_context.socket(zmq.PUSH)
            sock.connect(self.sink_addr)
            self.push_sockets[thread_id] = sock

        return self.push_sockets[thread_id]
    
    def _get_sub_socket(self) -> zmq.Socket:
        thread_id = threading.get_native_id()

        if thread_id not in self.sub_sockets:
            self.sub_sockets[thread_id] = self.local_context.socket(zmq.SUB)
            self.sub_sockets[thread_id].connect(self.publisher_addr)

        return self.sub_sockets[thread_id]

    def _get_client(self, network_id: str, request: 'Request') -> NetworkClient:
        if network_id not in self.clients:
            client = self.handle_connection(request, network_id)
            self.clients[network_id] = client
        return self.clients[network_id]

    def _get_id(self):
        if session.get("network_id") is None:
            id = uuid.uuid4().bytes
            session["network_id"] = id
        return session["network_id"]
    
    def _get_message_topic(self, message: Union[Request, Response]) -> str:
        return str(message.get_id()).encode()
