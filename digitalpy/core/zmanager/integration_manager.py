################
# Author: FreeTAKTeam
# The Integration manager receives all answers from all workers, prints them, and sends a message 
# to the workers to shut down when all tasks are complete.
# Uses a ZMQ_PULL socket to receive answers from the workers.
# Uses a ZMQ_PUB socket to send the FINISH message to the workers.
#
################


import zmq

class IntegrationManager:
    def __init__(self, integration_manager_puller_protocol: str, integration_manager_puller_address: str, integration_manager_puller_port: int,
                 integration_manager_publisher_protocol: str, integration_manager_publisher_address: str, integration_manager_publisher_port: int) -> None:
        self.integration_manager_puller_protocol = integration_manager_puller_protocol
        self.integration_manager_puller_address = integration_manager_puller_address
        self.integration_manager_puller_port = integration_manager_puller_port
        self.integration_manager_publisher_protocol = integration_manager_publisher_protocol
        self.integration_manager_publisher_address = integration_manager_publisher_address
        self.integration_manager_publisher_port = integration_manager_publisher_port


    def initialize_connections(self):
        context = zmq.Context()

        # create a pull socket
        pull_socket = context.socket(zmq.PULL)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        pull_socket.setsockopt(zmq.RCVHWM, 0)
        pull_socket.bind(f"{self.integration_manager_puller_protocol}://{self.integration_manager_puller_address}:{self.integration_manager_puller_port}")
        self.pull_socket = pull_socket

        # create a pub socket
        pub_socket = context.socket(zmq.PUB)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        pub_socket.setsockopt(zmq.SNDHWM, 0)
        pub_socket.bind(f"{self.integration_manager_publisher_protocol}://{self.integration_manager_publisher_address}:{self.integration_manager_publisher_port}")
        self.pub_socket = pub_socket

    def start(self):
        """this is the main running function for the integration manager"""
        self.initialize_connections()

        while True:
            try:
                # receive a message from a client
                request = self.pull_socket.recv_multipart()[0]
                response_protocol, response_object_unserialized = request.split(b',', 1)
                subject = b"/messages" + response_protocol

                try:
                    # send the response back to the client
                    self.pub_socket.send(subject + b" " + response_object_unserialized)
                except Exception as ex:
                    print("Error sending response to client: {}".format(ex))
            except Exception as ex:
                print("Error "+str(ex))