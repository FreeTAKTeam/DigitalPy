import logging
from typing import Optional

import zmq

from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.serialization.controllers.serializer_action_key import (
    SerializerActionKey,
)
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER,
)
from digitalpy.core.zmanager.controller_message import ControllerMessage
from digitalpy.core.zmanager.domain.model.zmanager_configuration import (
    ZManagerConfiguration,
)
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

RECIPIENT_DELIMITER = ";"


class IntegrationManagerSubscriber:
    """This class is responsible for managing subscription connections to the integration manager."""

    def __init__(
        self,
        formatter: Formatter,
        timeout: int,
        service_id: Optional[str] = None,
        application_protocol: Optional[str] = None,
    ):
        # list of connection to which the socket should reconnect after
        # being unpickled
        self.__subscriber_socket_connections = []

        self.subscriber_context: zmq.Context = None  # type: ignore
        self.subscriber_socket: zmq.Socket = None  # type: ignore
        self.subscriber_formatter = formatter
        self.logger = logging.getLogger(self.__class__.__name__)

        self.service_id = service_id
        self.application_protocol = application_protocol
        self.zmanager_conf: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )
        self.serializer_container: SerializerContainer = ObjectFactory.get_instance(
            "SerializerContainer"
        )

        self.timeout = timeout

        self.action_key_controller: ActionKeyController = ObjectFactory.get_instance(
            "ActionKeyController"
        )
        self.serializer_action_key: SerializerActionKey = ObjectFactory.get_instance(
            "SerializerActionKey"
        )

    def setup(self):
        """Connect or reconnect to integration manager"""

        # added to fix hanging connect issue as per
        # https://stackoverflow.com/questions/44257579/zeromq-hangs-in-a-python-multiprocessing-class-object-solution
        self.subscriber_context = zmq.Context()
        self.subscriber_socket = self.subscriber_context.socket(zmq.SUB)

        self.__subscriber_socket_connections.append(
            self.zmanager_conf.integration_manager_pub_address
        )

        # add the connection to the connections list so it can be reconnected upon serialization
        self.subscriber_socket.connect(
            self.zmanager_conf.integration_manager_pub_address
        )

        self._subscribe_to_topics()

        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.subscriber_socket.setsockopt(zmq.RCVHWM, 0)
        self.subscriber_socket.setsockopt(zmq.SNDHWM, 0)
        self.subscriber_socket.setsockopt(zmq.LINGER, 0)

        self.set_blocking(True)
        self.set_timeout(self.timeout)

    def _get_topics(self) -> list[ActionKey]:
        topics = []
        return topics

    def _subscribe_to_topics(self):
        for topic in self._get_topics():
            self.subscribe_to_action(topic)

    def subscribe_to_action(self, action_key: ActionKey):
        """Subscribe to a topic

        Args:
            action_key (ActionKey): the action key to subscribe to
        """
        topic = self.serializer_action_key.to_generic_topic(action_key)
        self.subscriber_socket.setsockopt(zmq.SUBSCRIBE, topic)

    def teardown(self):
        """Disconnect from broker"""
        for connection in self.__subscriber_socket_connections:
            self.subscriber_socket.disconnect(connection)
        self.subscriber_socket.close()
        self.subscriber_context.term()
        self.subscriber_context.destroy()

    def fetch_integration_manager_request(self) -> Optional[Request]:
        """receive the next response from the integration manager"""
        try:
            message = self._receive_message()

            return self._deserialize_request(message)
        except zmq.error.Again:
            return None

    def fetch_integration_manager_response(self) -> Optional[Response]:
        try:
            message = self._receive_message()

            return self._deserialize_response(message)
        except zmq.error.Again:
            return None
        
    def unsubscribe_from_topic(self, topic: bytes):
        """Unsubscribe from a topic"""
        self.subscriber_socket.setsockopt(zmq.UNSUBSCRIBE, topic)

    def _receive_message(self) -> bytes:
        message = self.subscriber_socket.recv_multipart()[0]

        return message

    def _deserialize_response(self, message: bytes) -> Response:
        response: Response = ObjectFactory.get_new_instance("Response")
        response = self.serializer_container.from_zmanager_message(message)
        return response

    def _deserialize_request(self, message: bytes) -> Request:
        request: Request = ObjectFactory.get_new_instance("Request")
        request = self.serializer_container.from_zmanager_message(message)
        return request

    def set_blocking(self, blocking: bool):
        """Set the blocking mode of the socket"""
        if blocking:
            self.subscriber_socket.setsockopt(zmq.RCVTIMEO, -1)
        else:
            self.subscriber_socket.setsockopt(zmq.RCVTIMEO, self.timeout)

    def set_timeout(self, timeout: int):
        """Set the timeout for the socket"""
        self.timeout = timeout
        self.subscriber_socket.setsockopt(zmq.RCVTIMEO, self.timeout)

    def __getstate__(self):
        state = self.__dict__
        if "subscriber_socket" in state:
            del state["subscriber_socket"]
        if "subscriber_context" in state:
            del state["subscriber_context"]
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.subscriber_context = zmq.Context()
        self.subscriber_socket = self.subscriber_context.socket(zmq.SUB)
        for connection in self.__subscriber_socket_connections:
            self.subscriber_socket.connect(connection)
            self.subscriber_socket.setsockopt_string(
                zmq.SUBSCRIBE, f"/messages/{self.service_id}/"
            )
            self.subscriber_socket.setsockopt_string(
                zmq.SUBSCRIBE, f"/commands/{self.service_id}/"
            )
