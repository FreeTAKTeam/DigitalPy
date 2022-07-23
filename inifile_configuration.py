from codecs import lookup_error
import os
import re
from tkinter import N

from configuration import Configuration


class InifileConfiguration(Configuration):
    def __init__(self, config_path, cache_path=None) -> None:
        self.__added_files = []
        self.config_path = config_path
        self.cache_path = cache_path

    def add_configuration(self, name, process_values=True):
        filename = self.config_path+name

        num_parsed_files = len(self.__added_files)

        if num_parsed_files>0:
            last_file = self.__added_files[num_parsed_files-1]
        else:
            last_file = ""

        if num_parsed_files>0 and last_file is filename and not self.check_file_date(self.__added_files, self.get_serialize_filename(self.__added_files)):
            return
        
        if not os.path.exists(filename):
            raise ValueError("Could not find configuration file")

        self.__added_files.append(filename)
        if not self.unserialize(self.__added_files):
            result = self.process_file(filename, self.config_array, self.contained_files)
            self.config_array = result['config']
            self.contained_files = sorted(set(result['files']))
            if process_values:
                self.process_values()

            self._build_lookup_table()

            self.serialize()

            self.config_changed()
        else:
            return

    def serialize(self):
        if not t

    def unserialize(self, parsed_files):
        if not self.is_modified(parsed_files) and self.file_exists(self.get_serialize_filename(parsed_files)):
            pass

    def get_config_path(self):
        return self.config_path

    def get_sections(self):
        return self.config_array.keys()

    def has_section(self, section):
        return self._lookup(section) != None

    def _build_lookup_table(self):
        self.lookup_table = {}
        for section, entry in self.config_array.items():
            lookup_section_key = section.lower()+":"
            self.lookup_table[lookup_section_key] = [section]
            for key, value in entry.items():
                lookup_key = lookup_section_key.lower()+key.lower()
                self.lookup_table[lookup_key] = [section, key]

    def get_sections(self):
        return self.config_array.keys()

    def has_value(self, key, section):
        return self._lookup(section, key) != None
    
    def get_value(self, key, section):
        lookup_entry = self._lookup(section, key)
        if lookup_entry is None or len(lookup_entry) == 1:
            raise Exception(f"No key {key} found in section {section}")
        else:
            return self.config_array[lookup_entry[0]][lookup_entry[1]]

    def get_boolean_value(self, key, section):
        value = self.get_value(key, section)
        return bool(value)
    
    def get_key(self, value, section):
        section_dict = self.get_section(section)
        map = {value: key for key, value in section_dict.items()}
        if value not in map:
            raise Exception(f"Value {value} not found in section {section}")
        return map[value]

    def get_section(self, section, include_meta=False):
        lookup_entry = self._lookup(section)
        if lookup_entry is None:
            raise Exception(f"section {section} not found")
        else:
            if include_meta:
                return self.config_array[lookup_entry[0]]
            else:
                return {key: val for key, val in self.config_array[lookup_entry[0]].items() if re.match('/^__/', key)}

    def _lookup(self, section, key=None):
        lookup_key = section.lower()+":"+key.lower()
        if lookup_key in self.lookup_table:
            return self.lookup_table[lookup_key]
        return None
