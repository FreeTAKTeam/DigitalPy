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

class IntegrationManagerPusher(Pusher):
    def __init__(self, formatter: Formatter):
        zmanager_configuration: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )
        super().__init__(formatter, zmanager_configuration.integration_manager_pull_address)
