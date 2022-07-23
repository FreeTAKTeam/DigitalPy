from action_key_provider import ActionKeyProvider
from configuration import Configuration


class ConfigActionKeyProvider(ActionKeyProvider):
    def __init__(self, configuration: Configuration, config_section):
        self.configuration = configuration
        self.config_section = config_section
        self.id = None

    def contains_key(self, action_key):
        return self.configuration.has_value(action_key, self.config_section)

    def get_key_value(self, action_key):
        if self.contains_key(action_key):
            return self.configuration.get_value(action_key, self.config_section)
        return None

    def get_id(self):
        if self.id == None:
            self.id = self.__class__.__name__+'.'+self.config_section