import zmq
import multiprocessing
import logging

from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.digipy_configuration.configuration import Configuration


class Subject:
    def __init__(
        self,
        routing_worker,
        configuration: Configuration,
        worker_count,
        frontend_pull_address,
        frontend_pub_address,
        backend_address,
        socket_timeout = 2000,
    ):
        self.workers = []
        self.configuration = configuration
        self.worker_count = worker_count
        self.worker = routing_worker
        self.frontend_pull_address = frontend_pull_address
        self.frontend_pub_address = frontend_pub_address
        self.backend_address = backend_address
        self.logger = logging.getLogger("DP-Subject_DEBUG")
        self.running = multiprocessing.Event()
        self.running.set()

        self.socket_timeout = socket_timeout

    def start_workers(self):
        for _ in range(self.worker_count):
            worker_process = multiprocessing.Process(
                target=self.worker.start, daemon=True
            )
            worker_process.start()
            self.workers.append(worker_process)

    def initiate_sockets(self):
        self.context = zmq.Context()
        self.backend_pusher = self.context.socket(zmq.PUSH)
        self.backend_pusher.bind(self.backend_address)
        self.backend_pusher.setsockopt(zmq.HEARTBEAT_IVL, 1000)
        self.backend_pusher.setsockopt(zmq.HEARTBEAT_TIMEOUT, 5000)
        self.backend_pusher.setsockopt(zmq.HEARTBEAT_TTL, 5000)

        self.frontend_pull = self.context.socket(zmq.PULL)
        self.frontend_pull.bind(self.frontend_pull_address)
        # set the timeout for the frontend pull socket so that the subject can check if it should stop periodically
        self.frontend_pull.setsockopt(zmq.RCVTIMEO, self.socket_timeout)

    def cleanup(self):
        self.backend_pusher.close()
        self.frontend_pull.close()
        self.context.term()

    def begin_routing(self):
        self.start_workers()
        self.initiate_sockets()
        while self.running.is_set():
            try:
                message = self.frontend_pull.recv_multipart()
                self.logger.debug("receieved %s",str(message))
                self.backend_pusher.send_multipart(message, copy=False)
            except zmq.error.Again:
                pass
            except Exception as ex:
                self.logger.fatal(
                    "exception thrown in subject %s", ex, exc_info=True)
        self.cleanup()

    def __getstate__(self):
        """delete objects that cannot be pickled or generally serialized"""
        state = self.__dict__.copy()
        if "backend_push" in state:
            del state["backend_push"]
        if "frontend_pull" in state:
            del state["frontend_pull"]
        if "workers" in state:
            del state["workers"]
        if "context" in state:
            del state["context"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.workers = []
