from uuid import uuid4

from digitalpy.routing.controller_message import ControllerMessage


class AbstractControllerMessage(ControllerMessage):    
    def __init__(self):
        self.sender = ""
        self.context = ""
        self.action = ""
        self.values = {}
        self.id = str(uuid4())
        self.properties = None
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
        raise NotImplementedError
    
    def clear_value(self, name):
        del self.values[name]
    
    def clear_values(self):
        self.values = {}
    
    def has_value(self, name):
        raise NotImplementedError
    
    def set_property(self, name, value):
        raise NotImplementedError
    
    def get_property(self, name):
        raise NotImplementedError
    
    def set_format(self, format):
        self.format = format
    
    def get_format(self):
        return self.format
