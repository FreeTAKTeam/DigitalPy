from abc import ABC, abstractmethod

class ControllerMessage(ABC):
    
    def __init__(self):
        self.sender = ""
        self.context = ""
        self.action = ""
        self.values = {}
        self.properties = None
        self.errors = None
    
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
    #
    # Set all key value pairs at once
    # @param values The associative array
    #/
    
    def set_values(self, values: dict):
        self.values = values
    #
    # Get a value
    # @param name The name of the variable
    # @param default The default value if the value is not defined or invalid while exceptions are suppressed (optional, default: _null_)
    # @param validateDesc An validation description to be used with Validator::validate() (optional, default: _null_)
    # @param suppressException Boolean whether to suppress a validation exception or not (optional, default: _false_)
    # @return The (filtered) value or default, if it does not exist
    #/
    
    def get_value(self, name, default=None):
        return self.values.get(name, default)
    #
    # Get a value as boolean
    # @param name The name of the variable
    # @param default The default value if the value is not defined (default: _false_)
    # @return The value or null if it does not exist
    #/
    
    def get_boolean_value(name, default=False):
        raise NotImplementedError
    #
    # Get all key value pairs
    # @return An associative array
    #/
    
    def get_values(self):
        return self.values
    #
    # Remove a value
    # @param name The name of the variable
    #/
    
    def clear_value(name):
        raise NotImplementedError
    #
    # Remove all values
    #/
    
    def clear_values():
        raise NotImplementedError
    #
    # Check for existence of a value
    # @param name The name of the variable
    # @return Boolean whether the value exists or not exist
    #/
    
    def has_value(name):
        raise NotImplementedError
    #
    # Set a property
    # @param name The name of the property
    # @param value The value of the property
    #/
    
    def set_property(name, value):
        raise NotImplementedError
    #
    # Get a property
    # @param name The name of the property
    # @return The property value or null
    #/
    
    def get_property(name):
        raise NotImplementedError