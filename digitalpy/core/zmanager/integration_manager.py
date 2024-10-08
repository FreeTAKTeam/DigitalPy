################
# Author: FreeTAKTeam
# The Integration manager receives all answers from all workers, prints them, and sends a message
# to the workers to shut down when all tasks are complete.
# Uses a ZMQ_PULL socket to receive answers from the workers.
# Uses a ZMQ_PUB socket to send the FINISH message to the workers.
#
################


import multiprocessing

import zmq

from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.zmanager.configuration.zmanager_constants import RESPONSE
from digitalpy.core.zmanager.configuration.zmanager_constants import PUBLISH_DECORATOR
from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.zmanager.domain.model.zmanager_configuration import (
    ZManagerConfiguration,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)
from digitalpy.core.main.factory import Factory


class IntegrationManager:
    """The Integration Manager is responsible for receiving messages from the workers and sending messages to the workers"""

    def __init__(
        self, factory: Factory, configuration_factory: ConfigurationFactory
    ) -> None:
        self.zmanager_configuration: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )
        self.context: zmq.Context
        self.pull_socket: zmq.Socket
        self.pub_socket: zmq.Socket
        self.running = multiprocessing.Event()
        self.running.set()
        self.action_key_controller: "ActionKeyController" = ObjectFactory.get_instance(
            "ActionKeyController"
        )

        self.serializer_container: "SerializerContainer" = ObjectFactory.get_instance(
            "SerializerContainer"
        )

        self.action_flow_controller: "ActionFlowController" = (
            ObjectFactory.get_instance("ActionFlowController")
        )
        self._factory = factory
        self._configuration_factory = configuration_factory
        self.response_action = self.action_key_controller.new_action_key()
        self.response_action.config = RESPONSE

    def initialize_connections(self):
        """initialize the connections for the integration manager"""
        self.context: zmq.Context = zmq.Context()

        # create a pull socket
        self._initialize_pull_socket()

        # create a pub socket
        self._initialize_pub_socket()

    def _initialize_pub_socket(self):
        self.pub_socket: zmq.Socket = self.context.socket(zmq.PUB)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.pub_socket.setsockopt(
            zmq.SNDHWM, self.zmanager_configuration.integration_manager_pub_sndhwm
        )
        self.pub_socket.bind(
            self.zmanager_configuration.integration_manager_pub_address
        )

    def _initialize_pull_socket(self):
        self.pull_socket: zmq.Socket = self.context.socket(zmq.PULL)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.pull_socket.setsockopt(
            zmq.RCVHWM, self.zmanager_configuration.integration_manager_pull_rcvhwm
        )
        self.pull_socket.bind(
            self.zmanager_configuration.integration_manager_pull_address
        )
        self.pull_socket.setsockopt(
            zmq.RCVTIMEO, self.zmanager_configuration.integration_manager_pull_timeout
        )

    def _setup(self):
        """setup the integration manager"""
        ObjectFactory.configure(self._factory)
        SingletonConfigurationFactory.configure(self._configuration_factory)
        self.initialize_connections()

    def _teardown(self):
        """cleanup the connections for the integration manager"""
        self.pull_socket.close()
        self.pub_socket.close()
        self.context.term()

    def start(self):
        """this is the main running function for the integration manager"""
        self._setup()

        while self.running.is_set():
            try:
                # receive a message from a client
                message = self.pull_socket.recv_multipart().pop(0)
                self._forward_message(message)
            except zmq.error.Again:
                pass
            except Exception as ex:
                print("Error " + str(ex))
        self._teardown()

    def _forward_message(self, message):
        c_message = self.serializer_container.from_zmanager_message(message)
        next_action = None
        new_message: bytes = message

        # check if the message is a publish message or if it has a config
        # if it is a publish message, leave it as is
        if c_message.decorator == PUBLISH_DECORATOR:
            next_action = c_message.action_key
        # otherwise, check if the message has a config and get the next action
        elif c_message.action_key.config:
            next_action = self.action_flow_controller.get_next_message_action(c_message)

        # TODO: this is probably a suboptimal solution, essentially we set a response action
        # which all services subscribe to.
        if next_action is None:
            c_message.action_key = self.response_action
            new_message = self.serializer_container.to_zmanager_message(c_message)
            self.pub_socket.send(message, copy=False)
        else:
            c_message.action_key = next_action
            new_message = self.serializer_container.to_zmanager_message(c_message)

        try:
            # send the response back to the client
            self.pub_socket.send(new_message, copy=False)

        except Exception as ex:
            print("Error sending response to client: {}".format(ex))
