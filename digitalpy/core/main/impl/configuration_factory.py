from importlib import import_module
from typing import Any, Optional

from digitalpy.core.serialization.controllers.serializer_action_key import (
    SerializerActionKey,
)
from digitalpy.core.digipy_configuration.domain.model.actionflow import ActionFlow
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
        self.action_flows: dict[str, ActionFlow] = {}
        self.serializer_action_key: SerializerActionKey = SerializerActionKey()

    def add_configuration(self, configuration: Configuration):
        """Register a new configuration in the factory by initializing all of it's referenced
        configuration objects.

        Args:
            configuration (Configuration): The configuration object to add.
        """
        for section_name in configuration.get_sections():
            self._initialize_configuration_section(configuration, section_name)
        self._publish_updates()

    def add_action_flow(self, action_flow: ActionFlow):
        """Add an action flow to the factory.

        Args:
            action_flow (ActionFlow): The action flow to add.
        """
        self.action_flows[action_flow.config_id] = action_flow

    def get_action_flow(self, config_id: str) -> Optional[ActionFlow]:
        """Get an action flow from the factory.

        Args:
            config_id (str): The id of the action flow to retrieve.

        Returns:
            Optional[ActionFlow]: The action flow.
        """
        return self.action_flows.get(config_id, None)

    def _publish_updates(self):
        """Publish updates to the configuration objects via the integration manager."""

    def get_configuration_object(self, name: str) -> Any:
        """Get a configuration object.

        Args:
            name (str): The name of the configuration object to retrieve.

        Returns:
            Any: The configuration object.
        """
        if name == ACTION_MAPPING_SECTION:
            return self.action_mapping
        else:
            return self.configuration_objects.get(name, None)

    def _initialize_configuration_section(
        self, configuration: Configuration, section_name: str
    ):
        """Initialize a configuration object. The section name is used to determine the
        type of configuration object and to call the correct initializer accordingly.

        Args:
            section (Configuration): The configuration section to initialize.
            section_name (str): The name of the configuration section.
        """
        if section_name == ACTION_MAPPING_SECTION:
            self._initialize_action_mapping_configuration_object(
                configuration, section_name
            )
        elif section_name in self.configuration_objects:
            self._extend_generic_configuration_object(configuration, section_name)
        else:
            self.configuration_objects[section_name] = (  # type: ignore
                self._initialize_generic_configuration_object(
                    configuration, section_name
                )
            )

    def _initialize_action_mapping_configuration_object(
        self, configuration: Configuration, section_name: str
    ):
        """Initialize an action mapping configuration object."""
        for key in configuration.get_section(section_name).keys():
            self.action_mapping[key] = (  # type: ignore
                self.serializer_action_key.deserialize_from_config_entry(
                    key, configuration.get_value(key, section_name)
                )
            )

    def _initialize_generic_configuration_object(
        self, configuration: Configuration, section_name: str
    ) -> Optional[Node]:
        """Initialize a generic configuration object.

        Args:
            configuration (Configuration): The configuration object to initialize.
            section_name (str): The name of the configuration section.

        Returns:
            Optional[Node]: The initialized configuration object.
        """
        try:
            class_path = configuration.get_value("__class", section_name)
        except KeyError:
            return None

        configuration_class = self._import_class(class_path)
        configuration_object = configuration_class(None, None)  # type: ignore
        properties = configuration_object.get_properties()

        for key in configuration.get_section(section_name).keys():
            if key in properties:
                setattr(
                    configuration_object,
                    key,
                    configuration.get_value(key, section_name),
                )

        return configuration_object

    def _extend_generic_configuration_object(
        self, configuration: Configuration, section_name: str
    ):
        """Extend a generic configuration object.

        Args:
            configuration (Configuration): The configuration object to extend.
            section_name (str): The name of the configuration section.

        Returns:
            Optional[Node]: The extended configuration object.
        """
        # iterate over the configuration section keys
        for key in configuration.get_section(section_name).keys():
            self._extend_property(configuration, section_name, key)

    def _extend_property(
        self, configuration: Configuration, section_name: str, key: str
    ):
        """Extend a property of a configuration object.

        Args:
            configuration (Configuration): The configuration object to extend.
            section_name (str): The name of the configuration section.
            key (str): The key of the property to extend.
        """
        # do not extend the class property
        if key == "__class":
            return

        # Get the configuration object property and the updated value
        cur_attr = getattr(self.configuration_objects[section_name], key, None)
        updated_attr = configuration.get_value(key, section_name)

        if isinstance(cur_attr, list) and not isinstance(updated_attr, list):
            # append the value to the list
            cur_attr.append(configuration.get_value(key, section_name))
        elif isinstance(cur_attr, list) and isinstance(updated_attr, list):
            # extend the list
            cur_attr.extend(configuration.get_value(key, section_name))
        else:
            #
            setattr(
                self.configuration_objects[section_name],
                key,
                configuration.get_value(key, section_name),
            )

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
