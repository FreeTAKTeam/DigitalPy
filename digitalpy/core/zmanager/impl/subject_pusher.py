import logging
from typing import TYPE_CHECKING

import zmq

from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.main.singleton_configuration_factory import \
    SingletonConfigurationFactory
from digitalpy.core.parsing.formatter import Formatter
from digitalpy.core.serialization.controllers.serializer_container import \
    SerializerContainer
from digitalpy.core.zmanager.domain.model.zmanager_configuration import \
    ZManagerConfiguration
from digitalpy.core.zmanager.pusher import Pusher

if TYPE_CHECKING:
    from digitalpy.core.zmanager.controller_message import ControllerMessage


class SubjectPusher(Pusher):
    """This class is responsible for communicating with the subject."""

    def __init__(self, formatter: Formatter, service_id: str = None):
        zmanager_configuration: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )
        super().__init__(formatter, zmanager_configuration.subject_pull_address)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.service_id = service_id

    def push_container(self, container: "ControllerMessage", service_id: str = ""):  # type: ignore
        """send the container object to the subject to the subject

        Args:
            container (ControllerMessage): the request to be sent to the subject
            protocol (str): the protocol of the request to be sent
            service_id (str, optional): the service_id of the request to be sent. Defaults to the id of the current service.
        """
        if service_id is None:
            service_id = self.service_id

        # set the service_id so it can be used to create the publish topic by the default routing worker
        container.sender = service_id
        super().push_container(container)
