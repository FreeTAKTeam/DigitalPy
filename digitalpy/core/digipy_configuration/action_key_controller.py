"""This module is responsible for controlling the action key models"""
import re
from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from digitalpy.core.zmanager.controller_message import ControllerMessage
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    ACTION_MAPPING_SECTION,
)
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER as DEL,
    DEFAULT_ENCODING,
)

class ActionKeyController:
    """This class is responsible controlling the action key models,
    this includes primarily, serialization and deserialization of the models.
    """

    def deserialize_from_ini(self, ini_key: str) -> ActionKey:
        """Deserialize the ini key to an ActionKey model from the format
        [Sender]?[context]@[Optional[decorator]]?[actopm][Optional=[target]]

        Args:
            ini_key (str): The ini key to deserialize

        Returns:
            ActionKey: The deserialized ActionKey model
        """
        action_key = self.new_action_key()
        
        pattern = r'(?P<sender>[^\?]+)\??(?P<context>[^\@]*)\@(?P<decorator>[^\?]*)\??(?P<action>[^\[]+)(?:\[(?P<target>[^\]]+)\])?'

        match = re.match(pattern, ini_key)
        if not match:
            raise ValueError("Invalid ini key format for action key " + ini_key)
        
        action_key.source = match.group("sender")
        action_key.context = match.group("context")
        action_key.decorator = match.group("decorator")
        action_key.action = match.group("action")
        action_key.target = match.group("target")
        return action_key

    def resolve_action_key(self, action_key: ActionKey) -> ActionKey:
        """Find the action key in the configuration which matches the given action key.

        Args:
            action_key (ActionKey): The action key to resolve

        Returns:
            ActionKey: The resolved action key

        Raises:
            ValueError: If no action key is found
        """
        action_mapping: dict[str, ActionKey] = SingletonConfigurationFactory.get_configuration_object(ACTION_MAPPING_SECTION)
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
        action_key = self.new_action_key()
        action_key.action = controller_message.get_action()
        action_key.context = controller_message.get_context()
        action_key.source = controller_message.get_sender()
        action_key.decorator = controller_message.get_decorator()
        return action_key

    def build_from_dictionary_entry(self, entry: tuple[str, str]) -> ActionKey:
        """Build an action key from a tuple.

        Args:
            action_key (tuple[str, str]): The tuple

        Returns:
            ActionKey: The action key
        """
        action_key = self.deserialize_from_ini(entry[0])
        action_key.target = entry[1]
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
