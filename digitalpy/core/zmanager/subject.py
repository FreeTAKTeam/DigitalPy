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
    ):
        self.workers = []
        self.configuration = configuration
        self.worker_count = worker_count
        self.worker = routing_worker
        self.frontend_pull_address = frontend_pull_address
        self.frontend_pub_address = frontend_pub_address
        self.backend_address = backend_address
        self.logger = logging.getLogger("DP-Subject_DEBUG")

    def start_workers(self):
        for _ in range(self.worker_count):
            worker_process = multiprocessing.Process(
                target=self.worker.start, daemon=True
            )
            worker_process.start()
            self.workers.append(worker_process)

    def initiate_sockets(self):
        print("initiate_sockets")
        self.context = zmq.Context()
        self.backend_pusher = self.context.socket(zmq.PUSH)
        self.backend_pusher.bind(self.backend_address)

        self.frontend_pull = self.context.socket(zmq.PULL)
        self.frontend_pull.bind(self.frontend_pull_address)

    def begin_routing(self):
        self.start_workers()
        self.initiate_sockets()
        while True:
            try:
                message = self.frontend_pull.recv_multipart()
                self.logger.debug("receieved %s",str(message))
                self.backend_pusher.send_multipart(message)
            except Exception as ex:
                self.logger.fatal("exception thrown in subject %s", ex, exc_info=1)

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
