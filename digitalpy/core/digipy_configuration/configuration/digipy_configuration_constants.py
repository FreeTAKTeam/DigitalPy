from string import Template
import pathlib

ACTION_MAPPING_SECTION = 'actionmapping'
MAX_FLOW_LENGTH = 100
ACTION_KEY = 'ActionKey'

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
