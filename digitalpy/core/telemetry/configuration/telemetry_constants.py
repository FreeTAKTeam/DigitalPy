""" this file contains all the constants used in the component """

import pathlib

from string import Template

COMPONENT_NAME = "telemetry"

CONFIGURATION_FORMAT = "json"

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).absolute().parent.parent

ACTION_MAPPING_PATH = CURRENT_COMPONENT_PATH / \
    "configuration/external_action_mapping.ini"
    
ACTION_FLOW_PATH = (
    CURRENT_COMPONENT_PATH / "configuration/telemetry_flows.ini"
)

INTERNAL_ACTION_MAPPING_PATH = CURRENT_COMPONENT_PATH / \
    "configuration/internal_action_mapping.ini"

LOGGING_CONFIGURATION_PATH = CURRENT_COMPONENT_PATH / "configuration/logging.conf"

LOG_FILE_PATH = CURRENT_COMPONENT_PATH / "logs"

MANIFEST_PATH = CURRENT_COMPONENT_PATH / "configuration/manifest.ini"

CONFIGURATION_PATH_TEMPLATE = Template(
    str(CURRENT_COMPONENT_PATH / "configuration/model_definitions/$message_type") +
    f".{CONFIGURATION_FORMAT}"
)

DB_PATH = "sqlite:///" + str(CURRENT_COMPONENT_PATH / "persistence/telemetry.db")
SYSTEMEVENT = "SystemEvent"
SYSTEMLOG = "SystemLog"
METRIC = "Metric"
SERVICESTATUS = "ServiceStatus"
STATUSFACTORY = "StatusFactory"
SYSTEMHEALTH = "SystemHealth"
TRACE = "Trace"
SPAN = "Span"
RESOURCE = "Resource"
ATTRIBUTE = "Attribute"
INSTRUMENTATIONLIBRARY = "InstrumentationLibrary"
ERROR = "Error"
