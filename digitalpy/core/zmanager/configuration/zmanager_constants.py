from enum import Enum


class TopicCategory(Enum):
    """The category of the topic"""

    CONTROLLER_MESSAGE = "ControllerMessage"
    SERVICE = "Service"
    REQUEST = "Request"
    RESPONSE = "Response"
    DEFAULT_ROUTING_WORKER = "DefaultRoutingWorker"


ZMANAGER_MESSAGE_DELIMITER = b"~"
ZMANAGER_MESSAGE_FORMAT = "pickled"
TOPIC = "Topic"
DEFAULT_ENCODING = "utf-8"

PUBLISH_DECORATOR = "PUBLISH"
