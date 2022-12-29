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
    def initialize_connections(self):
        context = zmq.Context()

        # create a pull socket
        pull_socket = context.socket(zmq.PULL)
        pull_socket.setsockopt(zmq.RCVHWM, 1000)  # limit the number of unprocessed requests that can be queued
        pull_socket.bind("tcp://127.0.0.1:12345")
        self.pull_socket = pull_socket

        # create a pub socket
        pub_socket = context.socket(zmq.PUB)
        pub_socket.setsockopt(zmq.SNDHWM, 1000)  # limit the number of unsent responses that can be queued
        pub_socket.bind("tcp://127.0.0.1:12346")
        self.pub_socket = pub_socket

    def main(self):
        self.initialize_connections()

        while True:
            # receive a message from a client
            request = self.pull_socket.recv()
            response_protocol, response_object_unserialized = request.split(b',', 1)
            subject = b"/"+response_protocol+b"/message"
            # measure the processing time of the request

            try:
                # send the response back to the client
                self.pub_socket.send(subject + b" " + response_object_unserialized)
            except Exception as ex:
                print(ex)