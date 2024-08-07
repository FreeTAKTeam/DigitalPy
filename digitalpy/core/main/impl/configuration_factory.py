from importlib import import_module
from typing import Any

from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    ACTION_MAPPING_SECTION,
)
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.domain.node import Node


class ConfigurationFactory:
    """ConfigurationFactory class to create and retrieve configuration objects."""

    def __init__(self):
        self.configuration_objects: dict[str, Node] = {}
        self.action_mapping: dict[str, ActionKey] = {}

    def add_configuration(self, configuration: Configuration):
        """Register a new configuration in the factory by initializing all of it's referenced configuration objects."""
        for section_name in configuration.get_sections():
            section = configuration.get_section(section_name)
            self._initialize_configuration_object(section, section_name)
        self._publish_updates()

    def _publish_updates(self):
        """Publish updates to the configuration objects via the integration manager."""

    def get_configuration_object(self, name: str) -> Any:
        """Get a configuration object."""
        if name == ACTION_MAPPING_SECTION:
            return self.action_mapping
        else:
            return self.configuration_objects.get(name, None)

    def _initialize_configuration_object(
        self, section: dict[str, str], section_name: str
    ) -> Node:
        """Initialize a configuration object. The section name is used to determine the type of configuration object and
        to call the correct initializer accordingly."""
        if section_name == ACTION_MAPPING_SECTION:
            return self._initialize_action_mapping_configuration_object(section)
        else:
            self.configuration_objects[section_name] = self._initialize_generic_configuration_object(section)

    def _initialize_action_mapping_configuration_object(
        self, section: dict[str, str]
    ) -> Node:
        """Initialize an action mapping configuration object."""
        action_mapping = {}
        for key in section:
            action_mapping[key] = self._deserialize_from_ini(section[key])
            
        return action_mapping

    def _deserialize_from_ini(self, ini_key: str) -> ActionKey:
        """Deserialize the ini key to an ActionKey model.

        Args:
            ini_key (str): The ini key to deserialize

        Returns:
            ActionKey: The deserialized ActionKey model
        """
        # TODO: This method should probably be moved to the ActionKeyController class however
        # in the current implementation this would cause a circular dependecy. I've brought this
        # up in https://github.com/orgs/FreeTAKTeam/projects/7/views/1?pane=issue&itemId=72571977
        # and this is a temporary solution.
        action_key = ActionKey(None, None)
        sections = ini_key.split("=")
        if len(sections) > 2:
            raise ValueError("Invalid ini key format for action key " + ini_key)
        elif len(sections) == 2:
            action_key.target = sections[1]

        key_sections = sections[0].split("?")
        if 3 > len(key_sections) or len(key_sections) > 4:
            raise ValueError("Invalid ini key format for action key " + ini_key)

        if len(key_sections) < 4:
            key_sections.insert(0, "")

        action_key.decorator = key_sections[0]
        action_key.action = key_sections[1]
        action_key.context = key_sections[2]
        action_key.source = key_sections[3]
        return action_key

    def _initialize_generic_configuration_object(self, section: dict[str, str]) -> Node:
        """Initialize a generic configuration object."""
        if section.get("__class", None) is None:
            return None

        configuration_class = self._import_class(section["__class"])
        configuration_object = configuration_class(None, None)
        propeties = configuration_object.get_properties()
        for key in section:
            if key in propeties:
                setattr(configuration_object, key, section[key])
        return configuration_object

    def _import_class(self, class_name: str) -> type[Node]:
        """Import a class."""
        parts = class_name.split(".")
        module = import_module(".".join(parts[:-1]))
        return getattr(module, parts[-1])

    def remove_configuration(self, config: Configuration):
        """Remove all configuration objects from the factory defined by passed config instance.

        Args:
            config (Configuration): The configuration object to remove.
        """
        for section_name in config.get_sections():
            self.configuration_objects.pop(section_name, None)
        self._publish_updates()
