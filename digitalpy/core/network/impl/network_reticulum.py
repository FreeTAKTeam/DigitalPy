"""This file contains the reticulum network implementation.
This consits of two main classes
1. reticulum manager which is responsible for running the reticulum network stack in a separate process and exposing to the network.
2. reticulum network which is responsible for exposing the network interface to a service
"""

import threading
import RNS
import LXMF
import os
import time
import zmq
from multiprocessing import Queue
from typing import Callable
from digitalpy.core.zmanager.response import Response
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.network.domain.client_status import ClientStatus
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.network.network_sync_interface import NetworkSyncInterface
from digitalpy.core.zmanager.request import Request

APP_NAME = LXMF.APP_NAME + ".delivery"

class AnnounceHandler:
    def __init__(self, identities):
        self.aspect_filter = APP_NAME  # Filter for LXMF announcements
        self.identities = identities  # Dictionary to store identities

    def received_announce(self, destination_hash, announced_identity, app_data):
        if destination_hash not in self.identities:
            self.identities[destination_hash] = announced_identity

class ReticulumNetwork(NetworkSyncInterface):
    def __init__(self):
        self._storage_path = None
        self._identity_path = None
        self._announcer_thread = None
        self.message_queue = Queue()
        self._clients = {}
        self._ret = None
        self._lxm_router = None
        self._identity = None
        self._my_identity = None
        self._identities = {}

    def initialize_network(self, _, _port, storage_path, identity_path, service_desc):
        self._storage_path = storage_path
        self._identity_path = identity_path
        self._ret = RNS.Reticulum()
        self._lxm_router = LXMF.LXMRouter(storagepath=self._storage_path)
        RNS.Transport.register_announce_handler(AnnounceHandler(self._identities))
        self._identity = self._load_or_generate_identity()
        self._my_identity = self._lxm_router.register_delivery_identity(self._identity)
        self._lxm_router.register_delivery_callback(self._ret_deliver)
        announcer_thread = threading.Thread(target=self._announcer)
        announcer_thread.start()
        self._service_desc = service_desc

    def _load_or_generate_identity(self):
        if os.path.exists(self._identity_path):
            try:
                return RNS.Identity.from_file(self._identity_path)
            except RNS.InvalidIdentityFile:
                pass
        identity = RNS.Identity()
        identity.to_file(self._identity_path)
        return identity

    def _get_client(self, identity: RNS.Identity) -> NetworkClient:
        if identity.hash in self._clients:
            return self._clients[identity.hash]
        else:
            client = self._register_new_client(identity.hash)
            self._clients[identity.hash] = client
            self._identities[identity.hash] = identity
            return client

    def _ret_deliver(self, message: LXMF.LXMessage):
        try:
            # validate the message
            if message.signature_validated:
                validated = True
            elif message.unverified_reason == LXMF.LXMessage.SIGNATURE_INVALID:
                validated = False
            elif message.unverified_reason == LXMF.LXMessage.SOURCE_UNKNOWN:
                validated = False
            else:
                validated = False

            # deliver the message to the network
            if validated and message.content is not None and message.content != b"":
                req: Request = ObjectFactory.get_new_instance("Request")
                req.set_value("body", message.content.decode("utf-8"))
                req.set_action("reticulum_message")
                req.set_value("client", self._get_client(message.source.identity))
                self.message_queue.put(req, block=False, timeout=0)
        except Exception as e:
            print(e)

    def _register_new_client(self, destination_hash: bytes):
        """Register a new client to the network.
        Args:
            destination_hash (bytes): The hash of the client destination to register.
        """
        oid = ObjectId("network_client", id=str(destination_hash))
        client: NetworkClient = ObjectFactory.get_new_instance(
            "DefaultClient", dynamic_configuration={"oid": oid}
        )
        client.id = destination_hash
        client.status = ClientStatus.CONNECTED
        client.service_id = self._service_desc.name
        client.protocol = self._service_desc.protocol
        return client

    def _get_client_identity(self, message: LXMF.LXMessage) -> bytes:
        """Get the identity of the client that sent the message. This is used for IAM and client tracking.
        Args:
            message (LXMF.LXMessage): The message to extract the identity from.

        Returns:
            bytes: The identity of the client as bytes
        """
        return message.source.identity.hash

    def _announcer(self, interval: int = 60):
        """Announce the reticulum network to the network."""
        while True:
            try:
                self._my_identity.announce()
            except Exception as e:
                pass
            time.sleep(interval)

    def _send_message_to_all_clients(self, message: str):
        for identity in self._clients.values():
            dest = RNS.Destination(
                self._identities[identity.id],
                RNS.Destination.OUT,
                RNS.Destination.SINGLE,
                "lxmf",
                "delivery",
            )
            msg = LXMF.LXMessage(
                destination=dest,
                source=self._my_identity,
                content=message.encode("utf-8"),
                desired_method=LXMF.LXMessage.DIRECT,
            )
            self._lxm_router.handle_outbound(msg)

    def _send_message_to_client(self, message: dict, client: NetworkClient):
        identity = self._identities.get(client.id)
        if identity is not None:
            dest = RNS.Destination(
                identity,
                RNS.Destination.OUT,
                RNS.Destination.SINGLE,
                "lxmf",
                "delivery",
            )
            msg = LXMF.LXMessage(
                destination=dest,
                source=self._my_identity,
                content=message.encode("utf-8"),
                desired_method=LXMF.LXMessage.DIRECT,
            )
            self._lxm_router.handle_outbound(msg)

    def service_connections(self, max_requests=1000, blocking=False, timeout=0):
        start_time = time.time()
        messages = []
        if self.message_queue.empty():
            return []
        messages.append(self.message_queue.get(block=blocking, timeout=timeout))
        while time.time() - start_time < timeout and len(messages) < max_requests:
            try:
                message = self.message_queue.get(block=False)
                messages.append(message)
            except Exception as e:
                break
        return messages
    
    def send_response(self, response):
        if response.get_value("client") is not None:
            self._send_message_to_client(response.get_value("message"), response.get_value("client"))
        else:
            self._send_message_to_all_clients(response.get_value("message"))

    def receive_message(self, blocking = False):
        return self.message_queue.get(block=blocking)
    
    def receive_message_from_client(self, client, blocking = False):
        raise NotImplementedError

    def teardown_network(self):
        pass
