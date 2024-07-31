from typing import Optional
from digitalpy.core.zmanager.controller_message import ControllerMessage
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    ACTION_MAPPING_SECTION,
)
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER as DEL,
    DEFAULT_ENCODING,
)

from digitalpy.core.parsing.formatter import Formatter


class ActionKeyController:
    """This class is responsible controlling the action key models,
    this includes primarily, serialization and deserialization of the models.
    """

    def __init__(self, configuration: Configuration, formatter: Formatter) -> None:
        self.configuration = configuration
        self.formatter = formatter

    def serialize_to_topic(self, action_key: ActionKey) -> bytes:
        """Serialize the model to a topic in the form
        of a string.

        Args:
            model (ActionKey): The model to serialize

        Returns:
            str: The action key serialized to a topic
        """
        ak = self.resolve_action_key(action_key)
        return (
            ak.decorator.encode(DEFAULT_ENCODING)
            + DEL
            + ak.source.encode(DEFAULT_ENCODING)
            + DEL
            + ak.context.encode(DEFAULT_ENCODING)
            + DEL
            + ak.action.encode(DEFAULT_ENCODING)
        )

    def serialize_to_generic_topic(self, action_key: ActionKey) -> bytes:
        """Serialize the model to a topic in the form
        of a string. This will be the most generic form of the topic. That means
        the returned topic will maintain the lowest level of specificity. This is
        useful when describing subscriptions.

        Args:
            model (ActionKey): The model to serialize

        Returns:
            str: The action key serialized to a topic
        """

        match (
            action_key.decorator,
            action_key.action,
            action_key.context,
            action_key.source,
        ):
            case (d, a, c, s) if d and a and c and s:
                return (
                    d.encode() + DEL + s.encode() + DEL + c.encode() + DEL + a.encode()
                )
            case (d, a, c, s) if d and s and c:
                return d.encode() + DEL + s.encode() + DEL + c.encode() + DEL
            case (d, a, c, s) if d and s:
                return d.encode() + DEL + s.encode() + DEL
            case (d, a, c, s) if d:
                return d.encode() + DEL
            case (_, _, _, _):
                return DEL + DEL + DEL + DEL

    def deserialize_from_topic(
        self, topic: bytes, encoding=DEFAULT_ENCODING
    ) -> tuple[ActionKey, bytes]:
        """Deserialize the topic to an ActionKey model.

        Args:
            topic (str): The topic to deserialize
            encoding (str, optional): The encoding to use. Defaults to DEFAULT_ENCODING.

        Returns:
            tuple[ActionKey, str]: The deserialized ActionKey model and the remaining topic if any
        """
        parts = topic.split(DEL, 4)
        action_key = self.new_action_key()
        if len(parts) < 3:
            raise ValueError(
                "Invalid topic format for action key " + topic.decode(encoding)
            )
        if len(parts) < 4:
            parts.insert(0, b"")
        action_key.decorator = parts[0].decode(encoding)
        action_key.action = parts[1].decode(encoding)
        action_key.context = parts[2].decode(encoding)
        action_key.source = parts[3].decode(encoding)

        return action_key, DEL.join(parts[4:])

    def deserialize_from_ini(self, ini_key: str) -> ActionKey:
        """Deserialize the ini key to an ActionKey model.

        Args:
            ini_key (str): The ini key to deserialize

        Returns:
            ActionKey: The deserialized ActionKey model
        """
        action_key = self.new_action_key()
        sections = ini_key.split("=")
        if len(sections) > 2:
            raise ValueError("Invalid ini key format for action key " + ini_key)
        elif len(sections) == 2:
            action_key.target = sections[1]

        key_sections = sections[0].split("?")
        if 3 > len(key_sections) or len(key_sections) > 4:
            raise ValueError("Invalid ini key format for action key " + ini_key)

        if len(key_sections) < 4:
            key_sections.insert(0, "")

        action_key.decorator = key_sections[0]
        action_key.action = key_sections[1]
        action_key.context = key_sections[2]
        action_key.source = key_sections[3]
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
        action_mapping: dict = self.configuration.get_section(ACTION_MAPPING_SECTION)
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

        ak = self.deserialize_from_ini(key)
        ak.target = action_mapping[key]
        ak.decorator = action_key.decorator
        return ak

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
        ak = self.resolve_action_key(action_key)
        return ak

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
