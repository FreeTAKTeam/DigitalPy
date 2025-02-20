import collections.abc
import os
import re
from io import StringIO, TextIOBase
from pathlib import PurePath
from threading import Lock, Condition
from typing import Any, Union

from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration


class InifileConfiguration(Configuration):
    """InifileConfiguration reads the application configuration from ini files.
    @note This class only supports ini files with sections.
    """

    def __init__(self, config_path, cache_path=None) -> None:
        self.__added_files = []
        self.config_path = config_path
        self.cache_path = cache_path
        self.config_array = {}
        self.contained_files = []
        self.lookup_table = {}
        self._lock = Lock()
        self._condition = Condition(lock=self._lock)

    # TODO: implement this method
    def get_configuration(self):
        raise NotImplementedError("get_configuration is not yet implemented")

    def add_configuration(
        self, name: Union[str, StringIO, PurePath], process_values=True
    ) -> None:
        """
        Args:
            name (str): the name of the configuration file to be added

        Raises:
            ValueError: raised if the file does not exist

        @note ini files referenced in section 'config' key 'include' are parsed
        afterwards
        """
        with self._lock:
            if isinstance(name, PurePath):
                name = str(name)
            filename = self.config_path + name

            num_parsed_files = len(self.__added_files)

            if num_parsed_files > 0:
                last_file = self.__added_files[num_parsed_files - 1]
            else:
                last_file = ""

            # if the last file is the same as the current file and the last file is not newer than the serialized data
            if (
                num_parsed_files > 0
                and last_file is filename
                and not self._check_file_date(
                    self.__added_files, self._get_serialize_filename(self.__added_files)
                )
            ):
                return

            if not os.path.exists(filename):
                raise ValueError("Could not find configuration file " + str(filename))

            self.__added_files.append(filename)
            result = self._process_file(
                filename, self.config_array, self.contained_files
            )
            self.config_array = result["config"]
            self.contained_files = sorted(set(result["files"]))

            self._build_lookup_table()
            self._condition.notify_all()

    def _check_file_date(self, file_list, reference_file) -> bool:
        """Check if one file in file_list is newer than the reference_file."""
        raise NotImplementedError("this method has not yet been implemented")

    def _get_serialize_filename(self, parsed_files):
        """Get the filename for the serialized data that correspond to the the given ini file sequence."""
        raise NotImplementedError("this method has not yet been implemented")

    def _config_changed(self):
        """Notify configuration change listeners"""
        raise NotImplementedError("this method has not yet been implemented")

    def _process_file(
        self,
        filename,
        config_array: Union[dict, None] = None,
        parsed_files: Union[list, None] = None,
    ) -> dict:
        """Process the given file recursively"""
        if config_array is None:
            config_array = {}
        if parsed_files is None:
            parsed_files = []
        if filename not in parsed_files:
            parsed_files.append(filename)
            # parse the file into a dictionary
            content = self.parse_ini_file(filename)
            # merge the config sections giving the new content precedence over the config array
            config_array = self._merge_dictionaries(config_array, content)
        self._condition.notify_all()
        return {"config": config_array, "files": parsed_files}

    def _merge_dictionaries(self, dict_one, dict_two):
        """merge two dictionaries, recursively

        Args:
            dict_one (dict): the subject dictionary
            dict_two (dict): the primary dictionary which takes precedence over dict_one
        """
        for k, v in dict_two.items():
            if isinstance(v, collections.abc.Mapping):
                dict_one[k] = self._merge_dictionaries(dict_one.get(k, {}), v)
            else:
                dict_one[k] = v
        return dict_one

    def get_config_includes(self, dictionary):
        """Search the given value for a 'include' key in a section named 'config' (case-insensivite)"""
        section_matches = None
        re.match("/(?:^|,)(config)(?:,|$)/i", dictionary.keys().join(","))

    def parse_ini_file(self, filename: str):
        """Load in the ini file specified in filename, and return the settings in a
        multidimensional array, with the section names and settings included. All
        section names and keys are lowercased.

        Args:
            filename (str): the path to the ini file to be parsed

        Raises:
            FileExistsError: raised if the file does not exist

        Returns:
            dict: an associative array containing the data

        Author:
            Sebastien Cevey <seb@cine_7.net> Original Code base: <info@megaman.nl> Added comment handling/Removed process sections flag: Ingo Herwig
        """
        if not os.path.exists(filename):
            raise FileExistsError
        config_array = {}
        section_name = ""
        with open(filename, "r", encoding="utf-8") as f:
            try:
                self.parse_ini_stream(config_array, f)
            except Exception as ex:
                raise ValueError(f"{filename} is invalid with error: {str(ex)}") from ex

        return config_array

    def parse_ini_stream(self, config_array: dict, stream: TextIOBase):
        """Parse the ini file stream and populate the config_array.

        Args:
            config_array (dict): the configuration array to be populated
            stream (TextIOBase): the stream to be parsed
        """
        lines = iter(stream.readlines())
        section_name = None
        key = None
        value = None
        for line in lines:
            line = line.strip()
            # ignore comments and empty lines
            if line == "" or line[0] == ";":
                continue
            # check for section
            if line.startswith("[") and line.endswith("]"):
                section_name = line[1:-1]
                config_array[section_name] = {}
                key = None
                value = None
            # check for key value pair
            elif "=" in line:
                parts = line.split("=", 1)
                key = parts[0].strip()
                value = parts[1].strip()
                # support for multi-line values e.g.:
                # key = [
                #   value1,
                #   value2
                # ]
                if value.startswith("[") and not value.endswith("]"):
                    while True:
                        line = next(lines).strip()

                        # ignore comments and empty lines
                        if line == "" or line[0] == ";":
                            continue
                        
                        if line.endswith("]"):
                            value+=line
                            break
                        value += line.strip()
                    config_array[section_name][key] = value
                else:
                    config_array[section_name][key] = value


    def get_config_path(self):
        """Get the file system path to the configuration files."""
        return self.config_path

    def get_sections(self):
        """Get the sections in the configuration."""
        return self.config_array.keys()

    def has_section(self, section: str) -> bool:
        """Check if a section exists in the configuration.

        Args:
            section (str): the name of the section to be checked

        Returns:
            bool: True if the section exists, False otherwise
        """
        return self._lookup(section) is not None

    def _build_lookup_table(self):
        """Build the internal lookup table"""
        for section, entry in self.config_array.items():
            lookup_section_key = section.lower() + ":"
            self.lookup_table[lookup_section_key] = [section]
            try:
                for key, value in entry.items():
                    lookup_key = lookup_section_key.lower() + key.lower()
                    self.lookup_table[lookup_key] = [section, key]
            except Exception as ex:
                raise ValueError(
                    f"section: {section} is invalid with error: {str(ex)}"
                ) from ex

    def has_value(self, key, section):
        return self._lookup(section, key) is not None

    def get_value(self, key: str, section: str) -> Union[str, list[str], list[float], float, bool]:
        """Get the value of a key in a section.
        
        Args:
            key (str): the name of the key to be retrieved
            section (str): the name of the section to be retrieved
        
        Raises:
            KeyError: raised if the key is not found
        
        Returns:
            Union[str, list[str], list[float], float, bool]: the value of the key in a type determined by the value
        """
        lookup_entry = self._lookup(section, key)
        if lookup_entry is None or len(lookup_entry) == 1:
            raise KeyError(f"No key {key} found in section {section}")
        else:
            raw_value = self.config_array[lookup_entry[0]][lookup_entry[1]]
            return self._convert_value(raw_value)

    def _convert_value(self, value: str) -> Union[str, list[str], list[float], float, bool]:
        """Convert the value to its appropriate type.
        
        Args:
            value (str): the value to be converted
        
        Returns:
            Union[str, list[str], list[float], float, bool]: the converted value
        """
        converters = [
            (self._is_boolean, self._convert_to_boolean),
            (self._is_list, self._convert_to_list),
            (self._is_float, self._convert_to_float),
        ]

        for check_func, convert_func in converters:
            if check_func(value):
                return convert_func(value)
        return value

    def _is_boolean(self, value: str) -> bool:
        """Check if the value is a boolean.
        
        Args:
            value (str): the value to be checked
        
        Returns:
            bool: True if the value is a boolean, False otherwise
        """
        return value.lower() in ["true", "false"]

    def _convert_to_boolean(self, value: str) -> bool:
        """Convert the value to a boolean.
        
        Args:
            value (str): the value to be converted
        
        Returns:
            bool: the converted value
        """
        return value.lower() == "true"

    def _is_list(self, value: str) -> bool:
        """Check if the value is a list.
        
        Args:
            value (str): the value to be checked
        
        Returns:
            bool: True if the value is a list, False otherwise
        """
        return value.startswith("[") and value.endswith("]")

    def _convert_to_list(self, value: str) -> list[Union[str, float]]:
        """Convert the value to a list.
        
        Args:
            value (str): the value to be converted
        
        Returns:
            list[Union[str, float]]: the converted value
        """
        value = value[1:-1]  # Remove the square brackets
        items = value.split(",")
        if all(self._is_float(item) for item in items):
            return [self._convert_to_float(item) for item in items]
        return [item.strip() for item in items]

    def _is_float(self, value: str) -> bool:
        """Check if the value is a float.
        
        Args:
            value (str): the value to be checked
        
        Returns:
            bool: True if the value is a float, False otherwise
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _convert_to_float(self, value: str) -> float:
        """Convert the value to a float.
        
        Args:
            value (str): the value to be converted
        
        Returns:
            float: the converted value
        """
        return float(value)

    def _is_boolean_value(self, key, section):
        """Check if a value is a boolean."""
        value = self.get_value(key, section)
        return value.lower() in ["true", "false"]

    def get_boolean_value(self, key, section):
        value = self.get_value(key, section)
        return bool(value)

    def get_list_value(self, key: str, section: str) -> list[str]:
        """ Get the value of a key in a section as a list.
        
        Args:
            key (str): the name of the key to be retrieved
            section (str): the name of the section to be retrieved
        
        Raises:
            KeyError: raised if the key is not found
        
        Returns:
            list[str]: the value of the key as a list
        """
        value = self.get_value(key, section)
        return value.replace(" ", "").replace("[", "").replace("]", "").split(",")

    def get_key(self, value, section):
        section_dict = self.get_section(section)
        map = {value: key for key, value in section_dict.items()}
        if value not in map:
            raise Exception(f"Value {value} not found in section {section}")
        return map[value]

    def get_section(self, section: str, include_meta=False) -> dict:
        """get a section from the configuration as a dictionary

        Args:
            section (str): the name of the section to be retrieved
            include_meta (bool, optional): whether or not to include values not prefixed by '__'. Defaults to False.

        Raises:
            ValueError: raised if the section is not found

        Returns:
            dict: a dictionary representing the contents of the section
        """
        lookup_entry = self._lookup(section)
        if lookup_entry is None:
            raise ValueError(f"section {section} not found")
        else:
            if include_meta:
                return self.config_array[lookup_entry[0]]
            else:
                return {
                    key: val
                    for key, val in self.config_array[lookup_entry[0]].items()
                    if not re.match("/^__/", key)
                }

    def _lookup(self, section: str, key: str = "") -> Union[list, None]:
        """Lookup section and key.

        Args:
            section (str): the name of the section to be looked up
            key (str, optional): the name of the key to be looked up. Defaults to "".

        Returns:
            list: a list containing the section and key if found, None otherwise
        """
        lookup_key = section.lower() + ":" + key.lower()
        if lookup_key in self.lookup_table:
            return self.lookup_table[lookup_key]
        # TODO: instead of returning None, should return an empty list
        return None

    def build_lookup_table(self) -> Any:
        """Build the internal lookup table"""
        self.lookup_table = {}
        for section, entry in self.config_array.items():
            lookup_section_key = section.lower() + ":"
            self.lookup_table[lookup_section_key] = [section]
            for key, _ in entry.items():
                lookup_key = lookup_section_key.lower() + key
                self.lookup_table[lookup_key] = {section: key}

    def check_file_date(self, file_list: Any, reference_file: Any) -> Any:
        """Check if one file in file_list is newer than the reference_file.
        @param $file_list An array of files
        @param $reference_file The file to check against
        @return True, if one of the files is newer, False else
        """
        raise NotImplementedError("this method has not yet been implemented")

    def config_changed(self) -> Any:
        """Notify configuration change listeners"""
        raise NotImplementedError("this method has not yet been implemented")

    def config_merge(self, array_1: Any, array_2: Any, override: Any) -> Any:
        """Merge the second array into the first, preserving entries of the first array
        unless the second array contains the special key '__inherit' set to False or
        they are re-defined in the second array.
           @param $array_1 First array.
           @param $array_2 Second array.
           @param $override Boolean whether values defined in array_1 should be
        overridden by values defined in array_2.
           @return The merged array.
        """
        raise NotImplementedError("this method has not yet been implemented")

    def get_configurations(self) -> Any:
        """@see Configuration::get_configurations()"""
        raise NotImplementedError("this method has not yet been implemented")

    def get_file_value(self, key: Any, section: Any) -> Any:
        """@see Configuration::get_file_value()"""
        raise NotImplementedError("this method has not yet been implemented")

    def get_serialize_filename(self, parsed_files: Any) -> Any:
        """Get the filename for the serialized data that correspond to the the given ini
        file sequence. NOTE: The method returns None, if no cache path is configured
           @param $parsed_files An array of parsed filenames
           @return String
        """
        raise NotImplementedError("this method has not yet been implemented")

    def is_editable(self, section: Any) -> Any:
        """@see WritableConfiguration::is_editable()"""
        raise NotImplementedError("this method has not yet been implemented")

    def is_modified(self) -> Any:
        """@see WritableConfiguration::is_modified()"""
        raise NotImplementedError("this method has not yet been implemented")

    def lookup(self, section: Any, key: Any = "") -> Any:
        """Lookup section and key.
           @param $section The section to lookup
           @param $key The key to lookup (optional)
           @return Array with section as first entry and key as second or None if not
        found
        """
        lookup_key = section.lower() + ":" + key.lower()
        if lookup_key in self.lookup_table:
            return self.lookup_table[lookup_key]
        else:
            return None

    def process_value(self, value: Any) -> Any:
        """Process the values in the ini array. This method turns string values that hold
        array definitions (comma separated values enclosed by curly brackets) into
        array values.
           @param $value A reference to the value
        """
        raise NotImplementedError("this method has not yet been implemented")

    def process_values(self) -> Any:
        """Process the values in the ini array. This method turns string values that hold
        array definitions (comma separated values enclosed by curly brackets) into
        array values.
        """
        raise NotImplementedError("this method has not yet been implemented")

    def remove_key(self, key: str, section: str) -> None:
        """@see WritableConfiguration::remove_key()"""
        lookup_entry = self._lookup(section, key)
        if lookup_entry is None:
            raise ValueError(f"key {key} not found in section {section}")
        else:
            del self.config_array[lookup_entry[0]][lookup_entry[1]]
            self._build_lookup_table()

    def remove_section(self, section: str) -> None:
        """@see WritableConfiguration::remove_section()"""
        lookup_entry = self._lookup(section)
        if lookup_entry is None:
            raise ValueError(f"section {section} not found")
        else:
            del self.config_array[lookup_entry[0]]
            self._build_lookup_table()

    def remove_configuration(self, name: str):
        """Remove a configuration and all of its sections and keys from the configuration.
        NOTE: This method does not remove the configuration file from the file system. n'or does it remove
        any keys which have been modified since the configuration was added.

        Args:
            name (str): the name of the configuration to be removed

        Raises:
            ValueError: raised if the configuration is not found
        """
        with self._lock:
            found = False
            for file in self.__added_files:
                if PurePath(file) == PurePath(name):
                    found = True
                    self.__added_files.remove(file)

            if not found:
                raise ValueError(f"Configuration {name} not found")

            # remove the keys defined in the configuration
            conf = {}
            self._process_file(name, conf, [])
            for section in conf.keys():
                self._remove_modified_section(conf, section)
            self._condition.notify_all()

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

    def rename_key(self, oldname: Any, newname: Any, section: Any) -> Any:
        """@see WritableConfiguration::rename_key()"""
        raise NotImplementedError("this method has not yet been implemented")

    def rename_section(self, oldname: Any, newname: Any) -> Any:
        """@see WritableConfiguration::rename_section()"""
        raise NotImplementedError("this method has not yet been implemented")

    def serialize(self) -> Any:
        """Store the instance in the file system. If the instance is modified, this call
        is ignored.
        """
        raise NotImplementedError("this method has not yet been implemented")

    def set_value(
        self, key: Any, value: Any, section: Any, create_section: Any = True
    ) -> Any:
        """@see WritableConfiguration::set_value()"""
        key = key.strip()
        if len(key) == 0:
            raise ValueError("Key cannot be empty")

        lookup_entry_section = self.lookup(section)
        if lookup_entry_section is None and not create_section:
            raise ValueError(f"section {section} does no exist")

        if lookup_entry_section is None and create_section:
            section = section.strip()
            self.config_array[section] = []
            final_section_name = section
        else:
            final_section_name = lookup_entry_section[0]
        if lookup_entry_section is not None:
            lookup_entry_key = self.lookup(section, key)
            if lookup_entry_key is None:
                final_key_name = key
            else:
                final_key_name = lookup_entry_key[1]
        else:
            final_key_name = key
        self.config_array[final_section_name][final_key_name] = value
        self._build_lookup_table()

    def unserialize(self, parsed_files: Any) -> Any:
        """Retrieve parsed ini data from the file system and update the current instance.
        If the current instance is modified or any file given in parsed_files is newer
        than the serialized data, this call is ignored. If InifileConfiguration class
        changed, the call will be ignored as well.
           @param $parsed_files An array of ini filenames that must be contained in the
        data.
           @return Boolean whether the data could be retrieved or not
        """
        raise NotImplementedError("this method has not yet been implemented")

    def write_configuration(self, name: Any) -> Any:
        """@see WritableConfiguration::write_configuration()"""
        raise NotImplementedError("this method has not yet been implemented")

    def get_directory_value(self, key: str, section: str):
        raise NotImplementedError("this method has not yet been implemented")

    def __str__(self) -> str:
        return str(self.config_array)

    def __getstate__(self) -> object:
        tmp_dict = self.__dict__.copy()
        if "_lock" in tmp_dict:
            del tmp_dict["_lock"]
        if "_condition" in tmp_dict:
            del tmp_dict["_condition"]

        return tmp_dict

    def __setstate__(self, tmp_dict: dict) -> None:
        self.__dict__.update(tmp_dict)
        self._lock = Lock()
        self._condition = Condition(lock=self._lock)
