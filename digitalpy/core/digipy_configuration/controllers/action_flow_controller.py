"""This module contains the ActionFlowController class.
"""

import re
from typing import Optional

from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.zmanager.controller_message import ControllerMessage
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)
from digitalpy.core.digipy_configuration.domain.model.actionflow import ActionFlow
from digitalpy.core.files.domain.model.file import File
from digitalpy.core.zmanager.configuration.zmanager_constants import DEFAULT_ENCODING
from digitalpy.core.serialization.controllers.serializer_action_key import (
    SerializerActionKey,
)


class ActionFlowController:
    """This is the ActionFlowController. It's responsibilities encompass all CRUD
    operations relating to action flows and access of these entities.
    """

    def __init__(self):
        self.action_key_controller = ActionKeyController()
        self.serializer_action_key = SerializerActionKey()

    def create_action_flow(self, file: File):
        """This operation parses the flow at the specified file and saves
        the result to the CofigurationFactory.
        """
        new_flow: ActionFlow
        for line in file.contents.splitlines():
            line_str = line.decode(DEFAULT_ENCODING)
            if line_str == "":
                continue
            elif re.match(r"^\[(.*)\]", line_str):
                new_flow = ActionFlow(None, None)
                new_flow.config_id = line_str[1:-1]
                SingletonConfigurationFactory.add_action_flow(new_flow)

            elif re.match(r"^[\w^\-_]*\?[\w^\-_]*(@[\w^\-_]+)?\?[\w^\-_]*", line_str):
                new_action = self.serializer_action_key.deserialize_from_ini(line_str)
                new_action.config = new_flow.config_id
                new_flow.actions.append(new_action)

            else:
                pass

    def get_next_action(
        self, controller_message: ControllerMessage
    ) -> Optional[ActionKey]:
        """This method will get the next action of the sequence referenced by the controller message.
        If the current Action is the final one, a None value will be returned
        """
        flow = SingletonConfigurationFactory.get_action_flow(
            controller_message.get_flow_name()
        )
        if flow is None:
            return None
        current_action = self.action_key_controller.build_from_controller_message(
            controller_message
        )
        i = 0
        for action in flow.actions:
            if action == current_action:
                current_action = action
                break
            i += 1
        if len(flow.actions) > i + 1:
            return flow.actions[i + 1]
        else:
            return None
