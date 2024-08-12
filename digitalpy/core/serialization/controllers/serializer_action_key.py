"""This module serializes and de-serializes actions and topics."""

from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)
from digitalpy.core.component_management.domain.model.actionkey import ActionKey
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER as DEL,
    DEFAULT_ENCODING,
)

STR_DEL = DEL.decode(DEFAULT_ENCODING)


class SerializerActionKey:
    """this class serializes and de-serializes actions and topics."""

    action_key: ActionKey

    def __init__(self):
        self.action_key_controller = ActionKeyController()

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
            action_key.config,
            action_key.decorator,
            action_key.action,
            action_key.context,
            action_key.source,
        ):
            case (co, d, a, c, s) if co and d and a and c and s:
                return_val = (
                    co.encode()
                    + DEL
                    + d.encode()
                    + DEL
                    + s.encode()
                    + DEL
                    + c.encode()
                    + DEL
                    + a.encode()
                )
            case (co, d, a, c, s) if co and d and s and c:
                return_val = (
                    co.encode()
                    + DEL
                    + d.encode()
                    + DEL
                    + s.encode()
                    + DEL
                    + c.encode()
                    + DEL
                )
            case (co, d, a, c, s) if co and d and s:
                return_val = co.encode() + DEL + d.encode() + DEL + s.encode() + DEL
            case (co, d, a, c, s) if co and d:
                return_val = co.encode() + DEL + d.encode() + DEL
            case (co, d, a, c, s) if co:
                return_val = co.encode() + DEL
            case (_, _, _, _):
                return_val = DEL + DEL + DEL + DEL
        return return_val

    def deserialize_from_topic(self, topic: bytes) -> tuple[ActionKey, bytes]:
        """Deserialize the topic to an ActionKey model and the remaining content."""
        parts = topic.split(DEL, 5)
        action_key = self.action_key_controller.new_action_key()
        if len(parts) < 3:
            raise ValueError("Invalid topic format for action key " + topic)
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
