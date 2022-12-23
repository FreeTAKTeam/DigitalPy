################
# Author: FreeTAKTeam
# The Integration manager receives all answers from all workers, prints them, and sends a message 
# to the workers to shut down when all tasks are complete.
# Uses a ZMQ_PULL socket to receive answers from the workers.
# Uses a ZMQ_PUB socket to send the FINISH message to the workers.
#
################


import logging
import timeit
import zmq

context = zmq.Context()

# create a pull socket
pull_socket = context.socket(zmq.PULL)
pull_socket.setsockopt(zmq.RCVHWM, 1000)  # limit the number of unprocessed requests that can be queued
pull_socket.bind("tcp://*:5555")

# create a pub socket
pub_socket = context.socket(zmq.PUB)
pub_socket.setsockopt(zmq.SNDHWM, 1000)  # limit the number of unsent responses that can be queued
pub_socket.bind("tcp://*:5556")

# create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def process_request(request):
    # process the request and return a response
    # ...
    return response

while True:
    # receive a message from a client
    request = pull_socket.recv()

    # measure the processing time of the request
    start_time = timeit.default_timer()

    try:
        # process the request
        response = process_request(request)

        # send the response back to the client
        pub_socket.send(response)

        # log the processing time of the request
        elapsed_time = timeit.default_timer() - start_time
        logger.info(f"Processed request in {elapsed_time:.2f} seconds")
    except Exception as e:
        #
