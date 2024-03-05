"""This file defines a class `TCPNetwork` that implements the `NetworkAsyncInterface`. This class is used to establish a network communication using the TCP protocol. It uses the ZeroMQ library for creating the socket and context for communication. 

The class has methods for initializing the network (`intialize_network`) and connecting a client to the server (`connect_client`). The `initialize_network` method sets up the ZeroMQ context and socket, binds it to the provided host and port. The `connect_client` method is used to connect a client to the server using the client's identity. 

The class also maintains a dictionary of clients connected to the network, with their identities as keys.
"""
import threading
from typing import Dict, List, TYPE_CHECKING, Union
import uuid
from flask import Blueprint, Flask, request as flask_request, session
import pickle
from digitalpy.core.digipy_configuration.configuration import Configuration

from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.network.domain.client_status import ClientStatus
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.service_management.domain.service_description import ServiceDescription

from digitalpy.core.network.network_sync_interface import NetworkSyncInterface
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

import zmq

if TYPE_CHECKING:
    from digitalpy.core.domain.domain_facade import Domain


class BlueprintCommunicator:
    """ this class should be used by the blueprints to communicate with the network"""

    # NOTE: the use of class variables in this case is several fold, firstly it is
    # to avoid duplicating creation of the sockets and contexts. Secondly we assume
    # that the network will be initialized before any blueprint is used.
    # Finally and most importantly we assume only one instance will exist per process,
    # this is because the network interface should be used by a service and each digitalpy
    # service is a process. This class is NOT thread safe between digitalpy services.
    # this is because the sink_addr is expected to only be set once by the network.
    sink_addr: Union[str, bytes]
    publisher_addr: Union[str, bytes]
    push_sockets: Dict[int, zmq.Socket] = {}
    sub_sockets: Dict[int, zmq.Socket] = {}
    local_context: zmq.Context = zmq.Context()

    def _get_id(self):
        if session.get("network_id") is None:
            id = uuid.uuid4().bytes
            session["network_id"] = id
        return session["network_id"]

    def _get_ctx(self) -> zmq.Context:
        if self.local_context is None:
            self.local_context = zmq.Context()
        return self.local_context

    def _get_sub_socket(self) -> zmq.Socket:
        thread_id = threading.get_native_id()

        if thread_id not in self.sub_sockets:
            self.sub_sockets[thread_id] = self._get_ctx().socket(zmq.SUB)
            self.sub_sockets[thread_id].connect(self.publisher_addr)

        return self.sub_sockets[thread_id]

    def _get_message_topic(self, message: Union[Request, Response]) -> bytes:
        return str(message.get_id()).encode()

    def _get_push_socket(self) -> zmq.Socket:
        thread_id = threading.get_native_id()

        if thread_id not in self.push_sockets:
            sock: zmq.Socket = self._get_ctx().socket(zmq.PUSH)
            sock.connect(self.sink_addr)
            self.push_sockets[thread_id] = sock

        return self.push_sockets[thread_id]

    def send_message_async(self, action: str, context: str, data: dict):
        """send a message to the network without waiting for a response

        Args:
            data (dict): _description_
            action (str): _description_
            context (str): _description_
        """
        push_sock = self._get_push_socket()

        req: Request = ObjectFactory.get_new_instance("Request")
        req.set_values(data)
        req.set_value("digitalpy_connection_id", self._get_id())
        req.set_action(action)
        req.set_context(context)
        push_sock.send_pyobj(req)

    def send_message_sync(self, data: dict, action: str, context: str) -> Response:
        """send a message to the network and wait for a response

        Args:
            data (dict): _description_
            action (str): _description_
            context (str): _description_

        Returns:
            Response: the response from the zmanager
        """
        # compose and send the request
        push_sock = self._get_push_socket()
        req: Request = ObjectFactory.get_new_instance("Request")
        req.set_values(data)
        req.set_value("digitalpy_connection_id", self._get_id())
        req.set_action(action)
        req.set_context(context)
        push_sock.send_pyobj(req)
        # wait for the response
        sub_sock = self._get_sub_socket()
        sub_sock.subscribe(self._get_message_topic(req))
        resp_raw = sub_sock.recv_multipart()
        resp = pickle.loads(resp_raw[1])
        sub_sock.unsubscribe(self._get_message_topic(req))
        return resp


class FlaskHTTPNetworkBlueprints(NetworkSyncInterface):
    """this class implements the NetworkAsyncInterface using the TCP protocol realizing
    the simplified approach to network communication, using Flask blueprints
    """

    def __init__(self):
        self.host: str = None  # type: ignore
        self.port: int = None  # type: ignore
        self.app: Flask = None  # type: ignore
        self.app_proc: threading.Thread = None  # type: ignore
        self.clients: Dict[bytes, NetworkClient] = {}
        self.local_context: zmq.Context
        self.sink: zmq.Socket
        self.publisher: zmq.Socket
        self.push_sockets: Dict[int, zmq.Socket] = {}
        self.sub_sockets: Dict[int, zmq.Socket] = {}
        self.service_desc: ServiceDescription = None  # type: ignore

    def intialize_network(self, host: str, port: int, blueprints: List[Blueprint], service_desc: ServiceDescription):
        self.service_desc = service_desc
        self.app = Flask(f"{host}:{port}")
        self.app.secret_key = str(uuid.uuid4())
        self.host = host
        self.port = port
        self.local_context = zmq.Context()
        self.sink = self.local_context.socket(zmq.PULL)
        self.publisher = self.local_context.socket(zmq.PUB)
        self.sink.bind_to_random_port(f"tcp://127.0.0.1")
        BlueprintCommunicator.sink_addr = self.sink.getsockopt(
            zmq.LAST_ENDPOINT)
        self.publisher.bind_to_random_port(f"tcp://127.0.0.1")
        BlueprintCommunicator.publisher_addr = self.publisher.getsockopt(
            zmq.LAST_ENDPOINT)

        for blueprint in blueprints:
            self.app.register_blueprint(blueprint)

        self.app_thread = threading.Thread(target=self._start_app, daemon=True)
        self.app_thread.start()

    def _start_app(self):
        self.app.run()

    def service_connections(self, max_requests=1000):
        requests = []
        for _ in range(max_requests):
            try:
                msg = self.receive_message(blocking=False)
                dp_conn_id = msg.get_value("digitalpy_connection_id")
                msg.set_value("client", self._get_client(dp_conn_id, msg))
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
        client.service_id = self.service_desc.id
        client.protocol = self.service_desc.protocol

        self.clients[network_id] = client

        return client

    def send_response(self, response: Response):
        self.publisher.send_multipart(
            [self._get_message_topic(message=response), pickle.dumps(response)])

    def _get_client(self, network_id: bytes, request: 'Request') -> NetworkClient:
        if network_id not in self.clients:
            client = self.handle_connection(request, network_id)
            self.clients[network_id] = client
        return self.clients[network_id]

    def _get_message_topic(self, message: Union[Request, Response]) -> bytes:
        return str(message.get_id()).encode()
