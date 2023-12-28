import pickle
import json
from typing import List
from digitalpy.core.IAM.controllers.iam_persistence_controller import IAMPersistenceController
from digitalpy.core.IAM.persistence.user import User
from digitalpy.core.domain.object_id import ObjectId

from digitalpy.core.main.controller import Controller
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.network.domain.client_status import ClientStatus
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from ..configuration.iam_constants import COMPONENT_NAME, CONNECTIONS_PERSISTENCE


class IAMUsersController(Controller):
    def __init__(self, request: Request, response: Response, action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, action_mapper, configuration)
        self.persistence_controller = IAMPersistenceController(
            request, response, action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        self.persistence_controller.initialize(request, response)
        super().initialize(request, response)

    def connection(self, connection: NetworkClient, *args, **kargs):
        """handle the case of a connection connection to any digitalpy service

        Args:
            connection (Node): the Node object associated with the connected connection
        """
        con_oid = str(connection.get_oid())
        user = User(id=con_oid, status=connection.status.value,
                    service_id=connection.service_id, protocol=connection.protocol)
        self.persistence_controller.save_user(user)

    def disconnection(self, connection_id: str, *args, **kwargs):
        """handle the case of a connection disconnection from any digitalpy service

        Args:
            connection (str): the id of the connection to be disconnected
        """
        user = self.persistence_controller.get_user(connection_id)
        self.persistence_controller.remove_user(user)

    def get_connections_by_id(self, connection_ids: List[str], *args, **kwargs) -> List[Node]:
        """get a list of connections by their ID's

        Args:
            connection_ids (List[str]): a list of IDs to be queries against the persistency layer
        """
        queried_connections: List[Node] = []

        for connection_id in connection_ids:

            user = self.persistence_controller.get_user(connection_id)
            connection = self._convert_user_to_network_client(user)
            queried_connections.append(connection)

        self.response.set_value("connections", queried_connections)

        return queried_connections

    def get_all_connections(self, *args, **kwargs) -> List[Node]:
        """get all recorded connections and save them to the connections value
        """
        users = self.persistence_controller.get_all_users()
        connections = []

        for user in users:
            connection = self._convert_user_to_network_client(user)
            connections.append(connection)

        self.response.set_value("connections", connections)

    def _convert_user_to_network_client(self, user: User) -> NetworkClient:
        """convert a user to a network client

        Args:
            user (User): the user to be converted

        Returns:
            NetworkClient: the converted user
        """
        oid = ObjectId.parse(user.id)
        if oid is None:
            raise ValueError("Invalid user id")

        connection = NetworkClient(oid=oid)

        connection.id = oid.get_id()[0][2:-1].encode()
        connection.service_id = user.service_id
        connection.status = ClientStatus[user.status]
        connection.protocol = user.protocol
        return connection
