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
        user = User(uid=con_oid, status=connection.status.value,
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
        queried_connections: List[Node] = [self._convert_user_to_network_client(self.persistence_controller.get_user(connection_id))
                                           for connection_id in connection_ids]

        self.response.set_value("connections", queried_connections)

        return queried_connections

    def authenticate_system_user(self, name: 'str', password: 'str', user_id: 'str', *args, **kwargs) -> bool:
        """authenticate a system user

        Args:
            user_id (User): the id of the user to be authenticated
        """

        if name is None or password is None:
            self.response.set_value("authenticated", False)
            return False

        system_user = self.persistence_controller.get_system_user_by_name(name)
        user = self.persistence_controller.get_user(user_id)
        if system_user is None:
            self.response.set_value("authenticated", False)
            return False

        if system_user.password != password:
            self.response.set_value("authenticated", False)
            return False

        self.response.set_value("authenticated", True)
        self.response.set_value(
            "message", f"{system_user.name} has been authenticated successfully.")
        self.persistence_controller.add_user_to_system_user(user, system_user)
        return True

    def validate_request(self, user: 'User', request: 'Request', action_key: str, *args, **kwargs) -> bool:
        """validate the request to ensure that the request is valid
        """
        for group in user.system_user.system_user_groups:
            for permission in group.system_groups.system_group_permissions:
                if permission.permissions.PermissionName == action_key:
                    return True

    def get_all_connections(self, *args, **kwargs) -> List[Node]:
        """get all recorded connections and save them to the connections value
        """
        users = self.persistence_controller.get_all_users()
        connections = [self._convert_user_to_network_client(
            user) for user in users]

        self.response.set_value("connections", connections)

    def _convert_user_to_network_client(self, user: User) -> NetworkClient:
        """convert a user to a network client

        Args:
            user (User): the user to be converted

        Returns:
            NetworkClient: the converted user
        """
        oid = ObjectId.parse(user.uid)
        if oid is None:
            raise ValueError("Invalid user id")

        connection = NetworkClient(oid=oid)

        connection.id = oid.get_id()[0][2:-1].encode()
        connection.service_id = user.service_id
        connection.status = ClientStatus[user.status]
        connection.protocol = user.protocol
        return connection
