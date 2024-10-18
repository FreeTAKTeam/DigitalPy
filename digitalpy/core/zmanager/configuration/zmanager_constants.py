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

# Signals that a message should be sent directly to the integration manager to be published
# bypasing the default routing worker
PUBLISH_DECORATOR = "PUBLISH"
# Signals that the action should not be executed sequentially and should instead be initiated
# by some response. This can be in conjunction with the prev_flow key when a sub-flow
# is called as part of the fulfillment of an action and we're not synchronously waiting for
# a response
ASYNC_DECORATOR = "ASYNC"

RESPONSE = "RESPONSE"
