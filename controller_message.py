from abc import ABC
from re import ABC

class ControllerMessage(ABC):
    def set_sender(self, sender):
        raise NotImplementedError

    def get_sender(self):
        raise NotImplementedError

    def set_context(self, context):
        raise NotImplementedError

    def get_context(self):
        raise NotImplementedError

    def get_action(self):
        raise NotImplementedError

    def set_action(self, action):
        raise NotImplementedError

    def set_format(self, format):
        raise NotImplementedError
    
    def get_format(self):
        raise NotImplementedError

    
    def set_value(name, value):
        """Set a value
        @param name The name of the variable
        @param value The value of the variable
        """
        raise NotImplementedError
    #
    # Set all key value pairs at once
    # @param values The associative array
    #/
    def set_values(values: dict):
        raise NotImplementedError
    #
    # Get a value
    # @param name The name of the variable
    # @param default The default value if the value is not defined or invalid while exceptions are suppressed (optional, default: _null_)
    # @param validateDesc An validation description to be used with Validator::validate() (optional, default: _null_)
    # @param suppressException Boolean whether to suppress a validation exception or not (optional, default: _false_)
    # @return The (filtered) value or default, if it does not exist
    #/
    def get_value(name, default=None, validateDesc=None, suppressException=False):
        raise NotImplementedError
    #
    # Get a value as boolean
    # @param name The name of the variable
    # @param default The default value if the value is not defined (default: _false_)
    # @return The value or null if it does not exist
    #/
    def getBooleanValue(name, default=False):
        raise NotImplementedError
    #
    # Get all key value pairs
    # @return An associative array
    #/
    def get_values():
        raise NotImplementedError
    #
    # Remove a value
    # @param name The name of the variable
    #/
    def clear_Value(name):
        raise NotImplementedError
    #
    # Remove all values
    #/
    def clear_Values():
        raise NotImplementedError
    #
    # Check for existence of a value
    # @param name The name of the variable
    # @return Boolean whether the value exists or not exist
    #/
    def has_Value(name):
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