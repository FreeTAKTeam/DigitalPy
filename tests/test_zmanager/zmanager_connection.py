import multiprocessing
import threading
import time
from typing import Optional
import zmq


class ServiceSimulatorMultiProc:
    """a test service that can send data to a subject and receive data from an integration manager, in a single process"""

    def __init__(
        self,
        subject_address: str,
        integration_manager_address: str,
        topics: list[str],
    ):
        self.copy = False
        self.subject_address = subject_address
        self.integration_manager_address = integration_manager_address
        self.topics = topics
        self.integration_manager_sock: Optional[zmq.Socket] = None
        self.subject_sock: Optional[zmq.Socket] = None

    def initiate_sockets(self):
        """initiate all socket connections"""
        context = zmq.Context()

        # initiate the subject socket
        self.subject_sock = context.socket(zmq.PUSH)
        self.subject_sock.connect(self.subject_address)

        # initiate the integration manager socket
        self.integration_manager_sock = context.socket(zmq.SUB)
        self.integration_manager_sock.connect(self.integration_manager_address)

        for topic in self.topics:
            self.integration_manager_sock.subscribe(topic)

    def start(self, messages: set[bytes]):
        """start the service"""
        self.initiate_sockets()
        sender = threading.Thread(target=self._send_messages, args=(messages,))
        receiver = threading.Thread(
            target=self._receive_messages, args=(len(messages),)
        )

        sender.start()
        receiver.start()

        sender.join()
        receiver.join()

    def _send_messages(self, messages: list[bytes]):
        """send messages to the subject"""
        [self.subject_sock.send_multipart([message], copy=self.copy) for message in messages]

    def _receive_messages(self, count: int):
        """receive messages from the integration manager"""
        [self.integration_manager_sock.recv_string() for _ in range(count)]

class ServiceSimulatorMultiProc:
    """a test service that can send data to a subject and receive data from an integration manager, in a single process"""

    def __init__(
        self,
        subject_address: str,
        integration_manager_address: str,
        topics: list[str],
    ):
        self.copy = False
        self.subject_address = subject_address
        self.integration_manager_address = integration_manager_address
        self.topics = topics
        self.integration_manager_sock: Optional[zmq.Socket] = None
        self.subject_sock: Optional[zmq.Socket] = None

    def initiate_subject_socket(self):
        """initiate the subject socket"""
        context = zmq.Context()
        self.subject_sock = context.socket(zmq.PUSH)
        self.subject_sock.connect(self.subject_address)

    def initiate_integration_manager_socket(self):
        """initiate the integration manager socket"""
        context = zmq.Context()
        self.integration_manager_sock = context.socket(zmq.SUB)
        self.integration_manager_sock.connect(self.integration_manager_address)

        for topic in self.topics:
            self.integration_manager_sock.subscribe(topic)

    def start(self, messages: set[bytes]):
        """start the service"""
        sender = multiprocessing.Process(target=self._send_messages, args=(messages,))
        receiver = multiprocessing.Process(
            target=self._receive_messages, args=(len(messages),)
        )

        receiver.start()
        time.sleep(0.1)
        sender.start()
        

        sender.join()
        receiver.join()

    def _send_messages(self, messages: set[bytes]):
        """send messages to the subject"""
        self.initiate_subject_socket()
        [self.subject_sock.send_multipart([message], copy=self.copy) for message in messages]

    def _receive_messages(self, count: int):
        """receive messages from the integration manager"""
        self.initiate_integration_manager_socket()
        [self.integration_manager_sock.recv_string() for _ in range(count)]
