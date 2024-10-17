import collections
import pathlib
from threading import Lock
from threading import Condition
from typing import Any
from ruamel.yaml import YAML

from digitalpy.core.files.impl.readable_file_wrapper import ReadableFileWrapper
from digitalpy.core.files.files_facade import Files
from digitalpy.core.files.domain.model.file import File
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration


class YamlConfiguration(Configuration):
    """A configuration implementation that reads YAML files and provides
    access to the configuration values."""

    def __init__(self, config_path: str, cache_path=None) -> None:
        self.__added_files: list[File] = []

        self.config_path = pathlib.Path(config_path)
        self.cache_path = cache_path

        self.config_array: dict[str, Any] = {}
        self.lookup_table = {}

        self._lock = Lock()
        self._condition = Condition(lock=self._lock)

        self.file_facade: Files = ObjectFactory.get_instance("Files")

    def get_configurations(self) -> list[File]:
        """Get a list of available configurations."""
        return self.__added_files

    def add_configuration(self, name: str, process_values: bool = True):
        """Parses the given configuration and merges it with already added configurations."""
        path = pathlib.Path(self.config_path, name)

        file = self.file_facade.get_file(str(path))

        if file in self.__added_files:
            return

        file_config = self._process_file(file)
        merged_config = self._merge_dictionaries(self.config_array, file_config)

        with self._lock:
            self.config_array = merged_config
            self.__added_files.append(file)
            self._condition.notify_all()

        self._build_lookup_table()

    def _process_file(self, file: File) -> dict[str, Any]:
        """Process a file and return the configuration as dictionary."""
        if file not in self.__added_files:
            return self._parse_yaml_file(file)
        else:
            return self.config_array

    def _parse_yaml_file(self, file: File) -> dict[str, Any]:
        yaml = YAML()
        return yaml.load(ReadableFileWrapper(file))
        
    def _merge_dictionaries(self, dict_one: dict, dict_two: dict) -> dict:
        """merge two dictionaries, recursively

        Args:
            dict_one (dict): the subject dictionary
            dict_two (dict): the primary dictionary which takes precedence over dict_one
        
        Returns:
            dict: the merged dictionary
        """
        return_dict = dict_one.copy()

        for k, v in dict_two.items():
            if isinstance(v, collections.abc.Mapping):
                return_dict[k] = self._merge_dictionaries(return_dict.get(k, {}), v)
            else:
                return_dict[k] = v
        return return_dict

    def _build_lookup_table(self):
        """Build the internal lookup table"""
        for section, entry in self.config_array.items():
            lookup_section_key = section.lower() + ":"
            self.lookup_table[lookup_section_key] = [section]
            try:
                for key, _ in entry.items():
                    lookup_key = lookup_section_key.lower() + key.lower()
                    self.lookup_table[lookup_key] = [section, key]
            except Exception as ex:
                raise ValueError(
                    f"section: {section} is invalid with error: {str(ex)}"
                ) from ex

    def get_sections(self) -> list[str]:
        """Get all section names."""
        return self.config_array.keys()

    def has_section(self, section: str) -> bool:
        """Check if a section exists."""
        return section in self.config_array

    def get_section(self, section: str, include_meta: bool = False) -> dict:
        """Get a section"""
        return self.config_array[section]

    def has_value(self, key: str, section: str) -> bool:
        """Check if a configuration value exists."""
        return key in self.config_array[section]

    def get_value(self, key: str, section: str) -> Any:
        """Get a configuration value."""
        return self.config_array[section][key]

    def get_boolean_value(self, key: str, section: str) -> bool:
        """Get a value from the configuration as boolean if it represents a boolean."""
        return bool(self.get_value(key, section))

    def get_directory_value(self, key: str, section: str) -> pathlib.Path:
        """Get a directory value from the configuration."""
        return pathlib.Path(self.get_value(key, section))

    def get_file_value(self, key: str, section: str) -> pathlib.Path:
        """Get a file value from the configuration.
        The value will interpreted as file relative to a base directory and
        returned as absolute path."""
        return self.config_path / pathlib.Path(self.get_value(key, section))

    def get_key(self, value: str, section: str) -> str:
        """Get a configuration key."""
        for key, val in self.config_array[section].items():
            if val == value:
                return key
        return None

    def set_value(self, key: str, value: Any, section: str):
        """Set a configuration value."""
        self.config_array[section][key] = value

    def remove_section(self, section: str):
        """Remove a section."""
        self.config_array.pop(section)

    def remove_key(self, key: str, section: str):
        """Remove a key from a section."""
        self.config_array[section].pop(key)

    def remove_configuration(self, name: str):
        """Remove a configuration and all of its sections and keys from the configuration.
        NOTE: This method does not remove the configuration file from the file system. n'or does it remove
        any keys which have been modified since the configuration was added.

        Args:
            name (str): the name of the configuration to be removed

        Raises:
            ValueError: raised if the configuration is not found
        """
        target_file = self.file_facade.get_file(str(pathlib.PurePath(self.config_path, name)))

        if target_file in self.__added_files:
            self.__added_files.remove(target_file)
        else:
            raise ValueError(f"Configuration {name} not found")
        
        # remove the keys defined in the configuration
        
        conf = self._process_file(target_file)
        for section in conf.keys():
            self._remove_modified_section(conf, section)

    def _remove_modified_section(self, conf: dict, section: str) -> None:
        """Remove a section from the configuration if it has not been modified since the configuration was added.

        Args:
            conf (dict): the configuration dictionary
            section (str): the name of the section to be

        Returns:
            None
        """
        items = self.get_section(section).items()
        if items == conf[section].items():
            self.remove_section(section)
        else:
            # remove only the keys that have not been modified
            for key, value in items:
                if value == conf[section].get(key):
                    self.remove_key(key, section)

    def save_configuration(self, name: str):
        """Save the entire configuration to the file system.

        Args:
            name (str): the name of the configuration to be saved

        Raises:
            ValueError: raised if the configuration is not found
        """
        target_file = self.file_facade.get_or_create_file(str(pathlib.PurePath(self.config_path, name)))

        yaml = YAML()
        yaml.dump(self.config_array, ReadableFileWrapper(target_file))

        self.file_facade.update_file(target_file)
