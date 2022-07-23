from abc import ABC

class ActionKeyProvider(ABC):
    def contains_key(self, action_key):
        raise NotImplementedError
    
    def get_key_value(self, action_key):
        raise NotImplementedError
    
    def get_id(self, action_key):
        raise NotImplementedError