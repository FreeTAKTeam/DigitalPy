"""Serialize Container Controller Module."""

from digitalpy.core.zmanager.response import Response
from digitalpy.core.serialization.controllers.serializer_action_key import (
    SerializerActionKey,
)
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    RESPONSE,
    ZMANAGER_MESSAGE_DELIMITER,
    ZMANAGER_MESSAGE_FORMAT,
)
from digitalpy.core.zmanager.controller_message import ControllerMessage


class SerializerContainer:
    """This class serializes a container object."""

    formatter: Formatter

    def __init__(self, formatter: Formatter):
        self.formatter = formatter
        self.serializer_action_key = SerializerActionKey()

    def to_zmanager_message(self, container: ControllerMessage) -> bytes:
        """Serialize the container to a ZManager message."""
        container.format = ZMANAGER_MESSAGE_FORMAT
        message_topic: bytes = self.serializer_action_key.to_topic(container.action_key)
        self.formatter.serialize(container)
        message_body: bytes = container.values

        return (
            message_topic
            + ZMANAGER_MESSAGE_DELIMITER
            + container.get_id().encode()
            + ZMANAGER_MESSAGE_DELIMITER
            + message_body
        )

    def from_zmanager_message(self, message: bytes) -> ControllerMessage:
        """Deserialize the container from a ZManager message."""
        action_key, message_body = self.serializer_action_key.deserialize_from_topic(
            message
        )

        request: Request = ObjectFactory.get_new_instance("Request")
        request.format = ZMANAGER_MESSAGE_FORMAT
        body_sections = message_body.split(ZMANAGER_MESSAGE_DELIMITER, maxsplit=1)
        request.set_id(body_sections[0].decode())
        request.set_values(body_sections[1])
        self.formatter.deserialize(request)
        request.action_key = action_key
        return request

    def from_zmanager_response(self, message: bytes) -> Response:
        """Deserialize the container from a ZManager response."""
        action_key, message_body = self.serializer_action_key.deserialize_from_topic(
            message
        )
        if action_key.config != RESPONSE:
            raise ValueError("The action key is not a response")
        response: Response = ObjectFactory.get_new_instance("Response")
        response.format = ZMANAGER_MESSAGE_FORMAT
        response.values = message_body
        body_sections = message_body.split(ZMANAGER_MESSAGE_DELIMITER, maxsplit=1)
        response.set_id(body_sections[0].decode())
        response.set_values(body_sections[1])
        self.formatter.deserialize(response)
        response.action_key = action_key
        return response
