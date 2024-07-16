from abc import ABC, abstractmethod
from typing import Any


class Configuration(ABC):
    """Implementations of Configuration give access to the application
    configuration. An instance of a Configuration implementation must
    be created on application startup and must be registered at ObjectFactory
    using the ObjectFactory.register_instance() method.

    Configurations are supposed to be separated into sections, that contain
    keys with values. Section names and keys are treated case insensitive.

    There maybe more than one application configuration.
    You can retrieve their names by using the Configuration.get_configurations()
    method. Different configurations maybe merged by calling the
    Configuration.add_configuration() method. While merging, existing values
    will be overwritten, while new values will be added. This allows
    to have very flexible application configurations for different scenarios,
    users and roles."""

    @abstractmethod
    def get_configurations(self) -> list:
        """Get a list of available configurations."""

    @abstractmethod
    def add_configuration(self, name: str, process_values: bool = True):
        """Parses the given configuration and merges it with already added configurations."""

    @abstractmethod
    def get_sections(self) -> list[str]:
        """Get all section names."""

    @abstractmethod
    def has_section(self, section: str) -> bool:
        """Check if a section exists."""

    @abstractmethod
    def get_section(self, section: str, include_meta: bool = False) -> dict:
        """Get a section"""

    @abstractmethod
    def has_value(self, key: str, section: str) -> bool:
        """Check if a configuration value exists."""

    @abstractmethod
    def get_value(self, key: str, section: str) -> Any:
        """Get a configuration value."""

    @abstractmethod
    def get_boolean_value(self, key, section):
        """Get a value from the configuration as boolean if it represents a boolean."""

    @abstractmethod
    def get_directory_value(self, key, section):
        """Get a directory value from the configuration."""

    @abstractmethod
    def get_file_value(self, key: str, section: str):
        """Get a file value from the configuration.
        The value will interpreted as file relative to a base directory and
        returned as absolute path."""

    @abstractmethod
    def get_key(self, value, section):
        """Get a configuration key."""

    @abstractmethod
    def set_value(self, key: str, value: Any, section: str):
        """Set a configuration value."""
