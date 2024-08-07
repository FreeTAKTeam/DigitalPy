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

from digitalpy.core.zmanager.domain.model.zmanager_configuration import ZManagerConfiguration
from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)
from digitalpy.core.main.factory import Factory


class IntegrationManager:
    def __init__(
        self,
        factory: Factory,
    ) -> None:
        self.zmanager_configuration: ZManagerConfiguration = SingletonConfigurationFactory.get_configuration_object(
            "ZManagerConfiguration"
        )
        self.context: zmq.Context
        self.pull_socket: zmq.Socket
        self.pub_socket: zmq.Socket
        self.running = multiprocessing.Event()
        self.running.set()
        self.action_key_controller: "ActionKeyController" = ObjectFactory.get_instance(
            "ActionKeyController"
        )
        self._factory = factory

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
        self.pub_socket.setsockopt(zmq.SNDHWM, self.zmanager_configuration.integration_manager_pub_sndhwm)
        self.pub_socket.bind(
            self.zmanager_configuration.integration_manager_pub_address
        )

    def _initialize_pull_socket(self):
        self.pull_socket: zmq.Socket = self.context.socket(zmq.PULL)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.pull_socket.setsockopt(zmq.RCVHWM, self.zmanager_configuration.integration_manager_pull_rcvhwm)
        self.pull_socket.bind(
            self.zmanager_configuration.integration_manager_pull_address
        )
        self.pull_socket.setsockopt(zmq.RCVTIMEO, self.zmanager_configuration.integration_manager_pull_timeout)

    def _setup(self):
        """setup the integration manager"""
        ObjectFactory.configure(self._factory)
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
                request = self.pull_socket.recv_multipart().pop(0)
                actionkey, body = self.action_key_controller.deserialize_from_topic(
                    request
                )
                topic = self.action_key_controller.serialize_to_topic(actionkey)

                try:
                    # send the response back to the client
                    self.pub_socket.send(
                        topic + ZMANAGER_MESSAGE_DELIMITER + body, copy=False
                    )
                except Exception as ex:
                    print("Error sending response to client: {}".format(ex))

            except zmq.error.Again:
                pass
            except Exception as ex:
                print("Error " + str(ex))
        self._teardown()
