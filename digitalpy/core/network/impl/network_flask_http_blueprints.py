
"""
This module defines two classes: `NetworkFlaskHTTPBlueprints` and `BlueprintCommunicator`. 

These classes implement the `NetworkSyncInterface` and are used to establish network 
communication using the TCP protocol with the help of the ZeroMQ library. 

The `NetworkFlaskHTTPBlueprints` class has methods for initializing the network 
and registering new client connections to the network. It also maintains a dictionary 
of clients connected to the network, with their identities as keys.

The `BlueprintCommunicator` class is not described in the initial excerpt, so its functionality 
will need to be documented once its methods and purpose are clear.

This module also imports necessary modules and types from Flask, typing, uuid, pickle, and various 
components from the `digitalpy` package.
"""
import threading
import pickle
import uuid
from typing import Dict, List, TYPE_CHECKING, Union
from flask import Blueprint, Flask, session

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
    """
    The BlueprintCommunicator class is designed to manage network communication for a service in
    a digitalpy environment.

    This class uses ZeroMQ sockets and contexts to establish and manage network communication. 
    It is designed to be used by a single service in a digitalpy environment, and is not 
    thread-safe between different services.

    The class maintains a dictionary of push and subscribe sockets for different network 
    identities, and also manages a local ZeroMQ context. The network addresses for the sink and 
    publisher are stored as class variables to be defined by the network at time of initialization.

    The class assumes that the network will be initialized before any blueprint is used, and 
    that the sink address will only be set once by the network.
    """

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

    def _get_id(self)->bytes:
        """ this method returns the network id for the current session

        Returns:
            bytes: the network id
        """
        if session.get("network_id") is None:
            net_id = uuid.uuid4().bytes
            session["network_id"] = net_id
        return session["network_id"]

    def _get_ctx(self) -> zmq.Context:
        """this method returns the local zmq context

        Returns:
            zmq.Context: the local zmq context
        """
        if self.local_context is None:
            self.local_context = zmq.Context()
        return self.local_context

    def _get_sub_socket(self) -> zmq.Socket:
        """this method returns the subscribe socket for the current thread

        Returns:
            zmq.Socket: the subscribe socket
        """
        thread_id = threading.get_native_id()

        if thread_id not in self.sub_sockets:
            self.sub_sockets[thread_id] = self._get_ctx().socket(zmq.SUB)
            self.sub_sockets[thread_id].connect(self.publisher_addr)

        return self.sub_sockets[thread_id]

    def _get_message_topic(self, message: Union[Request, Response]) -> bytes:
        """this method returns the topic for the message

        Args:
            message (Union[Request, Response]): the message

        Returns:
            bytes: the topic of the message
        """
        return str(message.get_id()).encode()

    def _get_push_socket(self) -> zmq.Socket:
        """this method returns the push socket for the current thread

        Returns:
            zmq.Socket: the push socket
        """
        thread_id = threading.get_native_id()

        if thread_id not in self.push_sockets:
            sock: zmq.Socket = self._get_ctx().socket(zmq.PUSH)
            sock.connect(self.sink_addr)
            self.push_sockets[thread_id] = sock

        return self.push_sockets[thread_id]

    def send_message_async(self, action: str, context: str, data: dict):
        """send a message to the network without returning a response

        Args:
            action (str): the action key for the request
            context (str): the context key for the request
            data (dict): the data to be sent as the values of the request
        """
        push_sock = self._get_push_socket()

        req: Request = ObjectFactory.get_new_instance("Request")
        req.set_values(data)
        req.set_value("digitalpy_connection_id", self._get_id())
        req.set_action(action)
        req.set_context(context)
        push_sock.send_pyobj(req)

    def send_message_sync(self, action: str, context: str, data: dict) -> Response:
        """send a message to the network and wait for a response

        Args:
            action (str): the action key for the request
            context (str): the context key for the request
            data (dict): the data to be sent as the values of the request

        Returns:
            Response: the response from the network
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
        self.app_thread: threading.Thread

    def intialize_network(self, host: str, port: int, blueprints: List[Blueprint], service_desc: ServiceDescription):
        """this method initializes the network

        Args:
            host (str): the host address
            port (int): the port number
            blueprints (List[Blueprint]): the list of blueprints to be registered
            service_desc (ServiceDescription): the service description
        """
        self.service_desc = service_desc
        self.app = Flask(f"{host}:{port}")
        self.app.secret_key = str(uuid.uuid4())
        self.host = host
        self.port = port
        self.local_context = zmq.Context()
        self.sink = self.local_context.socket(zmq.PULL)
        self.publisher = self.local_context.socket(zmq.PUB)
        self.sink.bind_to_random_port("tcp://127.0.0.1")
        BlueprintCommunicator.sink_addr = self.sink.getsockopt(
            zmq.LAST_ENDPOINT)
        self.publisher.bind_to_random_port("tcp://127.0.0.1")
        BlueprintCommunicator.publisher_addr = self.publisher.getsockopt(
            zmq.LAST_ENDPOINT)

        for blueprint in blueprints:
            self.app.register_blueprint(blueprint)

        self.app_thread = threading.Thread(target=self._start_app, daemon=True)
        self.app_thread.start()

    def _start_app(self):
        """this method starts the flask app"""
        self.app.run()

    def service_connections(self, max_requests=1000) -> List[Request]:
        """this method returns the requests from the network

        Args:
            max_requests (int, optional): the maximum number of requests to be returned. 
            Defaults to 1000.

        Returns:
            List[Request]: the list of requests
        """
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

    def receive_message(self, blocking: bool = False) -> Request:
        """this method receives a message from the network

        Args:
            blocking (bool, optional): whether the receive should be blocking. Defaults to False.

        Returns:
            Request: the message received
        """
        if blocking:
            return self.sink.recv_pyobj()
        else:
            return self.sink.recv_pyobj(zmq.NOBLOCK)

    def handle_connection(self, request: Request, network_id: bytes):
        """this method handles a connection request from the network

        Args:
            request (Request): the request
            network_id (bytes): the network id

        Returns:
            NetworkClient: the network client
        """
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
        """this method sends a response to the network

        Args:
            response (Response): the response
        """
        self.publisher.send_multipart(
            [self._get_message_topic(message=response), pickle.dumps(response)])

    def _get_client(self, network_id: bytes, request: 'Request') -> NetworkClient:
        """this method returns the client for the given network id

        Args:
            network_id (bytes): the network id
            request (Request): the request

        Returns:
            NetworkClient: the network client
        """
        if network_id not in self.clients:
            client = self.handle_connection(request, network_id)
            self.clients[network_id] = client
        return self.clients[network_id]

    def _get_message_topic(self, message: Union[Request, Response]) -> bytes:
        """this method returns the topic for the message

        Args:
            message (Union[Request, Response]): the message

        Returns:
            bytes: the topic of the message
        """
        return str(message.get_id()).encode()

    def receive_message_from_client(self, client: NetworkClient, blocking: TYPE_CHECKING = False) -> Request:
        """this method has not yet been implemented"""
        return super().receive_message_from_client(client, blocking)

    def teardown_network(self):
        """this method tears down the network"""
        self.sink.close()
        self.publisher.close()
        self.local_context.term()
