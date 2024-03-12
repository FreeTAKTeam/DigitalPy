from typing import Callable, Dict, List
from digitalpy.core.IAM.configuration.iam_constants import AUTHENTICATED_USERS, UNAUTHENTICATED_USERS
from digitalpy.core.IAM.controllers.iam_persistence_controller import IAMPersistenceController
from digitalpy.core.domain.node import Node
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.action_mapper import ActionMapper

class IAMGroupController(Controller):
    def __init__(
        self,
        request,
        response,
        sync_action_mapper,
        configuration,
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistency_controller = IAMPersistenceController(request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        self.persistency_controller.initialize(request, response)
        super().initialize(request, response)

    def create_default_groups(self, **kwargs):
        """this function is responsible for creating the default groups"""
        self.persistency_controller.create_group(AUTHENTICATED_USERS)
        self.persistency_controller.create_group(UNAUTHENTICATED_USERS)

    def validate_users(self, recipients: List[str], message: Node, **kwargs):
        """this function is responsible for validating that all users on
        a list are permitted to receive the content. If a user on the list
        isn't permitted to receive the message then it is removed from
        the users list.

        Args:
            users (List[str]): the list of users to which the model object is intended to be sent
            message (Node): the node intended to be sent to the clients
        """
        # TODO: currently this method isn't implemented but rather is
        # simply a placeholder which will be implemented once group
        # functionality is implemented
        self.response.set_value("recipients", recipients)