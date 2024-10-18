"""This module is responsible for controlling the action key models"""

import re
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.zmanager.controller_message import ControllerMessage
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    ACTION_MAPPING_SECTION,
)
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER as DEL,
    DEFAULT_ENCODING,
)
from digitalpy.core.serialization.controllers.serializer_action_key import (
    SerializerActionKey,
)


class ActionKeyController:
    """This class is responsible controlling the action key models,
    this includes primarily, serialization and deserialization of the models.
    """

    def __init__(self) -> None:
        self.serializer_action_key = SerializerActionKey()

    def resolve_action_key(self, action_key: ActionKey) -> ActionKey:
        """Find the action key in the configuration which matches the given action key.

        Args:
            action_key (ActionKey): The action key to resolve

        Returns:
            ActionKey: The resolved action key

        Raises:
            ValueError: If no action key is found
        """
        action_mapping: dict[str, ActionKey] = (
            SingletonConfigurationFactory.get_configuration_object(
                ACTION_MAPPING_SECTION
            )
        )
        match (action_key.source, action_key.context, action_key.action):
            case (s, c, a) if (s and c and a) and f"{s}?{c}?{a}" in action_mapping:
                key = f"{s}?{c}?{a}"
            case (s, c, a) if (s and a) and f"{s}??{a}" in action_mapping:
                key = f"{s}??{a}"
            case (s, c, a) if (c and a) and f"?{c}?{a}" in action_mapping:
                key = f"?{c}?{a}"
            case (s, c, a) if (s and c) and f"{s}?{c}?" in action_mapping:
                key = f"{s}?{c}?"
            case (s, c, a) if s and f"{s}??" in action_mapping:
                key = f"{s}??"
            case (s, c, a) if a and f"??{a}" in action_mapping:
                key = f"??{a}"
            case (s, c, a) if c and f"?{c}?" in action_mapping:
                key = f"?{c}?"
            case (_, _, _):
                raise ValueError("No action key found for " + str(action_key))

        return action_mapping[key]

    def build_from_controller_message(
        self, controller_message: ControllerMessage
    ) -> ActionKey:
        """Build an action key from a controller message.

        Args:
            controller_message (ControllerMessage): The controller message

        Returns:
            ActionKey: The action key
        """
        return controller_message.action_key

    def build_from_dictionary_entry(self, entry: tuple[str, str]) -> ActionKey:
        """Build an action key from a tuple.

        Args:
            action_key (tuple[str, str]): The tuple

        Returns:
            ActionKey: The action key
        """
        action_key = self.serializer_action_key.deserialize_from_config_entry(*entry)
        return action_key

    def new_action_key(self) -> ActionKey:
        """Get the action key model from the configuration.

        Args:
            action (str): The action
            context (str): The context
            source (str): The source

        Returns:
            ActionKey: The action key model
        """

        return ActionKey(None, None)
