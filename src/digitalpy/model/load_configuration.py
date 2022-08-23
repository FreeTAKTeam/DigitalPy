from argparse import ArgumentError
from dataclasses import dataclass, field
import os
from string import Template
import json
from typing import Dict

@dataclass
class Relationship:
    min_occurs: int = 0
    max_occurs: int = 1

@dataclass
class ConfigurationEntry:
    relationships: Dict[str, Relationship] = field(default_factory=dict)

@dataclass
class Configuration:
    elements: Dict[str, ConfigurationEntry] = field(default_factory=dict)

class LoadConfiguration:
    def __init__(self, configuration_path_template: Template):
        self.configuration_path_template = configuration_path_template

    def find_configuration(self, message_type):
        message_type = message_type.lower()
        message_configuration_path = self.configuration_path_template.substitute(message_type=message_type)
        if not os.path.exists(message_configuration_path):
            raise Exception("configuration for %s not found" % message_configuration_path)
        
        # TODO: extend with more configuration formats
        if message_configuration_path.endswith(".json"):
            return self.parse_json_configuration(message_configuration_path)
        else:
            raise Exception("configuration type not supported")

    def parse_json_configuration(self, message_configuration_path):
        with open(message_configuration_path, 'rb') as configuration_file:
            config = json.load(configuration_file)["definitions"]
            configuration = Configuration()
            for class_name, class_values in config.items():
                config_entry = ConfigurationEntry()
                for child_name, value in class_values["properties"].items():
                    if "$ref" in value:
                        child_name = value["$ref"].split("/")[-1]
                        config[child_name]
                        config_entry.relationships[child_name] = Relationship(value.get("minItems", 0), value.get("maxItems", 1))
                configuration.elements[class_name] = config_entry
        return configuration