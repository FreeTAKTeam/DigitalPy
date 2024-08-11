from abc import ABC
from uuid import uuid4
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey


class ControllerMessage(ABC):
    """A message that is sent to a controller"""

    def __init__(self):
        self.sender: str = ""
        self.context: str = ""
        self.action: str = ""
        self.decorator: str = ""
        self.flow_id: str
        self.values = {}
        self.id = str(uuid4())
        self.properties: dict
        self.errors = None
        self.format = ""

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def set_sender(self, sender):
        self.sender = sender

    def get_sender(self):
        return self.sender

    def set_context(self, context):
        self.context = context

    def get_context(self):
        return self.context

    def get_action(self):
        return self.action

    def set_action(self, action):
        self.action = action

    def set_value(self, name, value):
        """Set a value
        @param name The name of the variable
        @param value The value of the variable
        """
        self.values[name] = value

    def set_values(self, values: dict):
        self.values = values

    def get_values(self):
        return self.values

    def get_value(self, name, default=None):
        return self.values.get(name, default)

    def get_boolean_value(self, name, default=False):
        """Get a boolean value"""
        return bool(self.values.get(name, default))

    def clear_value(self, name):
        del self.values[name]

    def clear_values(self):
        self.values = {}

    def has_value(self, name):
        """Check if a value exists"""
        return name in self.values

    def set_property(self, name, value):
        """Set a property"""
        self.properties[name] = value

    def get_property(self, name):
        """Get a property"""
        return self.properties.get(name)

    def set_format(self, format):
        self.format = format

    def get_format(self):
        return self.format

    def set_decorator(self, decorator: str):
        """Set the decorator"""
        self.decorator = decorator

    def get_decorator(self):
        """Get the decorator"""
        return self.decorator
    
    def set_flow_id(self, flow_id: str):
        self.flow_id = flow_id
    
    def get_flow_id(self):
        return self.flow_id
    
    def set_action_key(self, action_key: ActionKey):
        self.set_action(action_key.action)
        self.set_context(action_key.context)
        self.set_sender(action_key.source)
        self.set_decorator(action_key.decorator)
