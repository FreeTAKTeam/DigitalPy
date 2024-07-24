import zmq


class TestRoutingWorker:
    """a test worker that routes messages from a subject to an integration manager without any processing"""

    def __init__(self, subject_address, integration_manager_address):
        self.subject_address = subject_address
        self.integration_manager_address = integration_manager_address

    def initiate_sockets(self):
        """initiate all socket connections"""
        context = zmq.Context()
        self.sock = context.socket(zmq.PULL)
        self.sock.connect(self.subject_address)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.sock.setsockopt(zmq.RCVHWM, 0)
        self.integration_manager_sock = context.socket(zmq.PUSH)
        self.integration_manager_sock.connect(self.integration_manager_address)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.integration_manager_sock.setsockopt(zmq.SNDHWM, 0)

    def start(self):
        self.initiate_sockets()
        while True:
            try:
                self.integration_manager_sock.send_multipart(self.sock.recv_multipart(), copy=False)
            except Exception as ex:
                print(f"exception thrown in worker {ex}")
