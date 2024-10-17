import json
import pathlib
from string import Template

CONFIGURATION_FORMAT = "json"

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).parent.parent.absolute()

CONFIGURATION_PATH_TEMPLATE = Template(
    str(
        pathlib.PurePath(
            CURRENT_COMPONENT_PATH, "configuration/model_definitions/$message_type"
        )
    )
    + f".{CONFIGURATION_FORMAT}"
)

LOGGING_CONFIGURATION_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/logging.conf")
)

LOG_FILE_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "logs")
)

ACTION_MAPPING_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH, "configuration/external_action_mapping.ini"
    )
)

INTERNAL_ACTION_MAPPING_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH, "configuration/internal_action_mapping.ini"
    )
)

BUSINESS_RULES_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/business_rules.json")
)

PERSISTENCE_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "persistence/emergencies.json")
)

MANIFEST_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/manifest.ini")
)

# time to wait until a service is manually terminated
SERVICE_WAIT_TIME = 10