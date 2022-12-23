from abc import ABC, abstractmethod

class ActionKeyProvider(ABC):
    """Implementations of ActionKeyProvider search for action keys."""
    
    @abstractmethod
    def contains_key(self, action_key: str):
        """Check if the given action key exists."""
    
    @abstractmethod
    def get_key_value(self, action_key: str):
        """Get the value of the given action key."""
    
    @abstractmethod
    def get_id(self):
        """Get a string value that uniquely describes the provider configuration."""
