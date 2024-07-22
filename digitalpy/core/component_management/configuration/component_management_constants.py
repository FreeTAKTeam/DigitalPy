""" this file contains all the constants used in the component """

import pathlib

from string import Template

COMPONENT_NAME = "component_management"

CONFIGURATION_FORMAT = "json"

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).absolute().parent.parent

ACTION_MAPPING_PATH = CURRENT_COMPONENT_PATH / \
    "configuration/external_action_mapping.ini"

INTERNAL_ACTION_MAPPING_PATH = CURRENT_COMPONENT_PATH / \
    "configuration/internal_action_mapping.ini"

LOGGING_CONFIGURATION_PATH = CURRENT_COMPONENT_PATH / "configuration/logging.conf"

LOG_FILE_PATH = CURRENT_COMPONENT_PATH / "logs"

MANIFEST_PATH = CURRENT_COMPONENT_PATH / "configuration/manifest.ini"

CONFIGURATION_PATH_TEMPLATE = Template(
    str(CURRENT_COMPONENT_PATH / "configuration/model_definitions/$message_type") +
    f".{CONFIGURATION_FORMAT}"
)

DB_PATH = "sqlite:///" + str(CURRENT_COMPONENT_PATH / "persistence/component_management.db")
COMPONENT_DOWNLOAD_PATH = CURRENT_COMPONENT_PATH / "persistence/downloads"
COMPONENT = "Component"
ACTIONKEY = "ActionKey"
ERROR = "Error"
MANIFEST = "manifest"
RELATIVE_MANIFEST_PATH = "configuration/manifest.ini"
DIGITALPY = "digitalpy"
REQUIRED_ALFA_VERSION = "requiredAlfaVersion"
NAME = "name"
VERSION = "version"
ID = "UUID"
VERSION_DELIMITER = "."
DEPENDENCIES = "dependencies"
DEPENDENCY_DELIMITER = ","