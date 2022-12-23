import zmq
import multiprocessing
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.config.configuration import Configuration


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
        self.backend_dealer = self.context.socket(zmq.DEALER)
        self.backend_dealer.bind(self.backend_address)

        self.frontend_pull = self.context.socket(zmq.PULL)
        self.frontend_pull.bind(self.frontend_pull_address)

        self.frontend_pub = self.context.socket(zmq.PUB)
        self.frontend_pub.bind(self.frontend_pub_address)

        self.poller = zmq.Poller()
        self.poller.register(self.backend_dealer, zmq.POLLIN)
        self.poller.register(self.frontend_pull, zmq.POLLIN)

    def begin_routing(self):
        self.initiate_sockets()
        self.start_workers()
        while True:
            socks = dict(self.poller.poll())

            if socks.get(self.frontend_pull) == zmq.POLLIN:
                message = self.frontend_pull.recv_multipart()
                message.insert(0, b"")
                self.backend_dealer.send_multipart(message)

            if socks.get(self.backend_dealer) == zmq.POLLIN:
                message = self.backend_dealer.recv_multipart()
                if message[0] == b"":
                    message = message[1:]
                print("publishing message to: " + str(message[0]))
                self.frontend_pub.send_multipart(message)

    def __getstate__(self):
        """delete objects that cannot be pickled or generally serialized"""
        state = self.__dict__.copy()
        if "backend_dealer" in state:
            del state["backend_dealer"]
        if "frontend_pull" in state:
            del state["frontend_pull"]
        if "frontend_pub" in state:
            del state["frontend_pub"]
        if "poller" in state:
            del state["poller"]
        if "workers" in state:
            del state["workers"]
        if "context" in state:
            del state["context"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.workers = []
