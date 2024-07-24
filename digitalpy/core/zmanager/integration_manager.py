################
# Author: FreeTAKTeam
# The Integration manager receives all answers from all workers, prints them, and sends a message
# to the workers to shut down when all tasks are complete.
# Uses a ZMQ_PULL socket to receive answers from the workers.
# Uses a ZMQ_PUB socket to send the FINISH message to the workers.
#
################


import multiprocessing
from typing import Optional

import zmq

from digitalpy.core.zmanager.configuration.zmanager_constants import \
    ZMANAGER_MESSAGE_DELIMITER


class IntegrationManager:
    def __init__(
        self,
        integration_manager_puller_protocol: str,
        integration_manager_puller_address: str,
        integration_manager_puller_port: int,
        integration_manager_publisher_protocol: str,
        integration_manager_publisher_address: str,
        integration_manager_publisher_port: int,
        timeout=3000,
    ) -> None:
        self.integration_manager_puller_protocol = integration_manager_puller_protocol
        self.integration_manager_puller_address = integration_manager_puller_address
        self.integration_manager_puller_port = integration_manager_puller_port
        self.integration_manager_publisher_protocol = (
            integration_manager_publisher_protocol
        )
        self.integration_manager_publisher_address = (
            integration_manager_publisher_address
        )
        self.integration_manager_publisher_port = integration_manager_publisher_port
        self.context: Optional[zmq.Context] = None
        self.pull_socket: Optional[zmq.Socket] = None
        self.pub_socket: Optional[zmq.Socket] = None
        self.running = multiprocessing.Event()
        self.running.set()
        self.timeout = timeout

    def initialize_connections(self):
        """initialize the connections for the integration manager"""
        self.context = zmq.Context()

        # create a pull socket
        self.pull_socket = self.context.socket(zmq.PULL)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.pull_socket.setsockopt(zmq.RCVHWM, 0)
        self.pull_socket.bind(
            f"{self.integration_manager_puller_protocol}://{self.integration_manager_puller_address}:{self.integration_manager_puller_port}"
        )
        self.pull_socket.setsockopt(zmq.RCVTIMEO, self.timeout)

        # create a pub socket
        self.pub_socket = self.context.socket(zmq.PUB)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.pub_socket.setsockopt(zmq.SNDHWM, 0)
        self.pub_socket.bind(
            f"{self.integration_manager_publisher_protocol}://{self.integration_manager_publisher_address}:{self.integration_manager_publisher_port}"
        )

    def cleanup(self):
        """cleanup the connections for the integration manager"""
        self.pull_socket.close()
        self.pub_socket.close()
        self.context.term()

    def start(self):
        """this is the main running function for the integration manager"""
        self.initialize_connections()

        while self.running.is_set():
            try:
                # receive a message from a client
                request = self.pull_socket.recv_multipart().pop(0)
                
                response_protocol, response_object_unserialized = request.split(
                    ZMANAGER_MESSAGE_DELIMITER, 1
                )
                subject = b"/messages" + response_protocol
                try:
                    # send the response back to the client
                    self.pub_socket.send(
                        subject + b" " + response_object_unserialized, copy=False
                    )
                except Exception as ex:
                    print("Error sending response to client: {}".format(ex))
            except zmq.error.Again:
                pass
            except Exception as ex:
                print("Error " + str(ex))
        self.cleanup()
