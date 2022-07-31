from abc import ABC

class Configuration(ABC):
    def get_configurations(self):
        raise NotImplementedError

    def get_sections(self):
        raise NotImplementedError

    def has_value(self, key, section):
        raise NotImplementedError
    
    def get_value(self, key, section):
        raise NotImplementedError

    def get_boolean_value(self, key, section):
        raise NotImplementedError
        
    def get_key(self, value, section):
        raise NotImplementedError