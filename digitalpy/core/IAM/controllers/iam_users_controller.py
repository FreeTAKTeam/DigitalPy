import pickle
import json
from typing import List

from digitalpy.core.main.controller import Controller
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from ..configuration.iam_constants import COMPONENT_NAME, CONNECTIONS_PERSISTENCE

class IAMUsersController(Controller):
    def __init__(self, request: Request, response: Response, action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, action_mapper, configuration)

    def connection(self, logger, connection: NetworkClient, **kargs):
        """handle the case of a connection connection to any digitalpy service
        
        Args:
            connection (Node): the Node object associated with the connected connection
        """
        con_oid = str(connection.get_oid())
        logger.debug("adding %s to persistency", con_oid)
        connections = self._load_persistency()
        # need to decode the pickled text so that it can be saved
        connections[con_oid] = connection
        self._update_persistency(connections=connections)

    def disconnection(self, logger, connection_id: str, **kwargs):
        """handle the case of a connection disconnection from any digitalpy service

        Args:
            connection (str): the id of the connection to be disconnected
        """
        logger.debug("removing %s from persistency", connection_id)
        connections = self._load_persistency()
        del connections[connection_id]
        self._update_persistency(connections=connections)

    def get_connections_by_id(self, connection_ids: List[str]) -> List[Node]:
        """get a list of connections by their ID's

        Args:
            connection_ids (List[str]): a list of IDs to be queries against the persistency layer
        """
        queried_connections: List[Node] = []
        
        connections = self._load_persistency()
        for connection_id in connection_ids:
            if connection_id in connections:
                queried_connections.append(connections[connection_id])

        self.response.set_value("connections", queried_connections)

        return queried_connections

    def get_all_connections(self, **kwargs) -> List[Node]:
        """get all recorded connections and save them to the connections value
        """
        connections = self._load_persistency()
        self.response.set_value("connections", list(connections.values()))

    def _load_persistency(self) -> dict:
        """load the contents of the persistency file

        Returns:
            dict: all persisted connections
        """
        try:
            with open(CONNECTIONS_PERSISTENCE, "rb+") as f:
                return pickle.load(f)
        # in the case that the file contains unreadable data
        # or no file exists return an empty dictionary which will later be written to the
        # file
        except EOFError:
            return {}
        except FileNotFoundError:
            return {}

    def _update_persistency(self, connections: dict):
        """update the persistency with changes

        Args:
            clients (dict): a dictionary of all clients
        """
        with open(CONNECTIONS_PERSISTENCE, "wb+") as f:
            pickle.dump(connections, f)