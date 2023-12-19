from abc import ABC, abstractmethod
from typing import Any
class ControllerMessage(ABC):
    
    @abstractmethod
    def get_id(self):
        return self.id
    
    @abstractmethod
    def set_id(self, id):
        self.id = id
    
    @abstractmethod
    def set_sender(self, sender):
        self.sender = sender

    @abstractmethod
    def get_sender(self):
        return self.sender
    
    @abstractmethod
    def set_context(self, context):
        self.context = context
    
    @abstractmethod
    def get_context(self):
        return self.context

    @abstractmethod
    def get_action(self):
        return self.action

    @abstractmethod
    def set_action(self, action):
        self.action = action
    
    @abstractmethod
    def set_value(self, name, value):
        """Set a value
        @param name The name of the variable
        @param value The value of the variable
        """
    
    @abstractmethod
    def set_values(self, values: dict):
        """set all key value pairs at once"""
    
    @abstractmethod
    def get_values(self):
        """get all key value pairs at once"""
    
    @abstractmethod
    def get_value(self, name, default=None) -> Any:
        """Get a value"""
    
    @abstractmethod
    def get_boolean_value(self, name, default=False):
        """Get a value as boolean"""

    @abstractmethod
    def clear_value(self, name):
        """Remove a value"""
        
    @abstractmethod
    def clear_values(self):
        """Remove all values"""
        
    @abstractmethod
    def has_value(self, name):
        """Check for existence of a value"""
        
    @abstractmethod
    def set_property(self, name, value):
        """Set a property"""
        
    @abstractmethod
    def get_property(self, name):
        """Get a property"""