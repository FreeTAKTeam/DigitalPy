"""This module serializes and de-serializes actions and topics."""

import re
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER as DEL,
    DEFAULT_ENCODING,
)

STR_DEL = DEL.decode(DEFAULT_ENCODING)


class SerializerActionKey:
    """this class serializes and de-serializes actions and topics."""

    action_key: ActionKey

    def __init__(self):
        pass

    def to_topic(self, action_key: ActionKey) -> bytes:
        """Serialize the model to a topic in the form of a string."""
        return (
            action_key.config
            + STR_DEL
            + action_key.decorator
            + STR_DEL
            + action_key.source
            + STR_DEL
            + action_key.context
            + STR_DEL
            + action_key.action
        ).encode(DEFAULT_ENCODING)

    def to_generic_topic(self, action_key: ActionKey) -> bytes:
        """Serialize the model to a topic in the form
        of a string. This will be the most generic form of the topic. That means
        the returned topic will maintain the lowest level of specificity. This is
        useful when describing subscriptions."""
        return_val: bytes
        match (
            action_key.action,
            action_key.context,
            action_key.source,
        ):
            case (a, c, s) if a and c and s:
                return_val = s.encode() + DEL + c.encode() + DEL + a.encode()
            case (a, c, s) if s and c:
                return_val = s.encode() + DEL + c.encode()
            case (a, c, s) if s:
                return_val = s.encode()
            case (_, _, _):
                return_val = b""
        if return_val:
            return_val = DEL + return_val
        match (
            action_key.decorator,
            action_key.config,
        ):
            case (d, c) if d and c:
                return_val = c.encode() + DEL + d.encode() + return_val
            case (d, c) if d:
                return_val = DEL + d.encode() + return_val
            case (d, c) if c:
                return_val = c.encode() + DEL + return_val
            case (_, _):
                return_val = return_val
        return return_val

    def deserialize_from_topic(self, topic: bytes) -> tuple[ActionKey, bytes]:
        """Deserialize the topic to an ActionKey model and the remaining content. a topic is in the form
        config/decorator/source/context/action/content where content contains the rest of the message
        information."""
        parts = topic.split(DEL, maxsplit=5)
        action_key = ActionKey(None, None)
        if len(parts) < 3:
            raise ValueError(
                "Invalid topic format for action key " + topic.decode(DEFAULT_ENCODING)
            )
        # optional decorator
        if len(parts) < 4:
            parts.insert(0, b"")
        # optional config
        if len(parts) < 5:
            parts.insert(0, b"")
        action_key.config = parts[0].decode(DEFAULT_ENCODING)
        action_key.decorator = parts[1].decode(DEFAULT_ENCODING)
        action_key.source = parts[2].decode(DEFAULT_ENCODING)
        action_key.context = parts[3].decode(DEFAULT_ENCODING)
        action_key.action = parts[4].decode(DEFAULT_ENCODING)

        return action_key, DEL.join(parts[5:])

    def deserialize_from_config_entry(self, key: str, val: str) -> ActionKey:
        """Deserialize the config entry to an ActionKey model."""
        ak = self.deserialize_from_ini(key)
        ak.target = val
        return ak

    def deserialize_from_ini(self, ini_key: str) -> ActionKey:
        """Deserialize the ini key to an ActionKey model from the format
        [Sender]?[context]@[Optional[decorator]]?[action][Optional[=target]]

        Args:
            ini_key (str): The ini key to deserialize

        Returns:
            ActionKey: The deserialized ActionKey model
        """
        action_key = ActionKey(None, None)

        pattern = r"^(?P<sender>[\w^-_]*)\?(?P<context>[\w^-_]*)(@?(?P<decorator>[\w^-_]*))\?(?P<action>[\w^-_]*)\s*(=\s*(?P<target>[\w\.]*))?"

        match = re.match(pattern, ini_key)
        if not match:
            raise ValueError("Invalid ini key format for action key " + ini_key)

        action_key.source = match.group("sender")
        action_key.context = match.group("context")
        action_key.decorator = match.group("decorator")
        action_key.action = match.group("action")
        action_key.target = match.group("target")
        return action_key
