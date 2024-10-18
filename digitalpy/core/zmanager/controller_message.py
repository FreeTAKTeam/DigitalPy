from abc import ABC
from uuid import uuid4
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey


class ControllerMessage(ABC):
    """A message that is sent to a controller"""

    def __init__(self):
        self.action_key: ActionKey = ActionKey(None, None)
        self.values = {}
        self.properties: dict
        self.errors = None
        self.format = ""
        self._message_id = str(uuid4())

    @property
    def decorator(self):
        return self.action_key.decorator

    @decorator.setter
    def decorator(self, decorator):
        self.action_key.decorator = decorator

    @property
    def sender(self):
        return self.action_key.source

    @sender.setter
    def sender(self, sender):
        self.action_key.source = sender

    @property
    def context(self):
        return self.action_key.context

    @context.setter
    def context(self, context):
        self.action_key.context = context

    @property
    def action(self):
        return self.action_key.action

    @action.setter
    def action(self, action):
        self.action_key.action = action

    @property
    def flow_name(self):
        return self.action_key.config

    @flow_name.setter
    def flow_name(self, flow_name):
        self.action_key.config = flow_name

    @property
    def id(self):
        return self._message_id

    @id.setter
    def id(self, message_id):
        self._message_id = message_id

    def get_id(self):
        """Get the unique identifier of the message.

        Returns:
            str: The unique identifier of the message.
        """
        return self._message_id

    def set_id(self, message_id):
        """Set the unique identifier of the message.

        Args:
            message_id (str): The unique identifier to set.
        """
        self._message_id = message_id

    def set_sender(self, sender):
        """Set the sender of the message.

        Args:
            sender (str): The sender to set.
        """
        self.action_key.source = sender

    def get_sender(self):
        """Get the sender of the message.

        Returns:
            str: The sender of the message.
        """
        return self.action_key.source

    def set_context(self, context):
        """Set the context of the message.

        Args:
            context (str): The context to set.
        """
        self.action_key.context = context

    def get_context(self):
        """Get the context of the message.

        Returns:
            str: The context of the message.
        """
        return self.action_key.context

    def get_action(self):
        """Get the action of the message.

        Returns:
            str: The action of the message.
        """
        return self.action_key.action

    def set_action(self, action):
        """Set the action of the message.

        Args:
            action (str): The action to set.
        """
        self.action_key.action = action

    def set_value(self, name: str, value: any):
        """Set a value in the message.

        Args:
            name (str): The name of the variable.
            value: The value of the variable.
        """
        self.values[name] = value

    def set_values(self, values: dict):
        """Set multiple values in the message.

        Args:
            values (dict): A dictionary of values to set.
        """
        self.values = values

    def get_values(self):
        """Get all values in the message.

        Returns:
            dict: A dictionary of all values in the message.
        """
        return self.values

    def get_value(self, name, default=None):
        """Get a specific value from the message.

        Args:
            name (str): The name of the variable.
            default: The default value to return if the variable is not found.

        Returns:
            The value of the variable, or the default value if not found.
        """
        return self.values.get(name, default)

    def get_boolean_value(self, name, default=False):
        """Get a boolean value from the message.

        Args:
            name (str): The name of the variable.
            default (bool): The default value to return if the variable is not found.

        Returns:
            bool: The boolean value of the variable, or the default value if not found.
        """
        return bool(self.values.get(name, default))

    def clear_value(self, name):
        """Clear a specific value from the message.

        Args:
            name (str): The name of the variable to clear.
        """
        del self.values[name]

    def clear_values(self):
        """Clear all values from the message."""
        self.values = {}

    def has_value(self, name):
        """Check if a specific value exists in the message.

        Args:
            name (str): The name of the variable to check.

        Returns:
            bool: True if the variable exists, False otherwise.
        """
        return name in self.values

    def set_property(self, name, value):
        """Set a property in the message.

        Args:
            name (str): The name of the property.
            value: The value of the property.
        """
        self.properties[name] = value

    def get_property(self, name):
        """Get a specific property from the message.

        Args:
            name (str): The name of the property.

        Returns:
            The value of the property, or None if not found.
        """
        return self.properties.get(name)

    def set_format(self, format):
        """Set the format of the message.

        Args:
            format (str): The format to set.
        """
        self.format = format

    def get_format(self):
        """Get the format of the message.

        Returns:
            str: The format of the message.
        """
        return self.format

    def set_decorator(self, decorator: str):
        """Set the decorator of the message.

        Args:
            decorator (str): The decorator to set.
        """
        self.decorator = decorator

    def get_decorator(self):
        """Get the decorator of the message.

        Returns:
            str: The decorator of the message.
        """
        return self.decorator

    def set_flow_name(self, flow_name: str):
        """Set the flow name of the message.

        Args:
            flow_name (str): The flow name to set.
        """
        self.action_key.config = flow_name

    def get_flow_name(self):
        """Get the flow name of the message.

        Returns:
            str: The flow name of the message.
        """
        return self.action_key.config

    def set_action_key(self, action_key: ActionKey):
        """Set the action key of the message.

        Args:
            action_key (ActionKey): The action key to set.
        """
        self.set_action(action_key.action)
        self.set_context(action_key.context)
        self.set_sender(action_key.source)
        self.set_decorator(action_key.decorator)
        self.set_flow_name(action_key.config)
