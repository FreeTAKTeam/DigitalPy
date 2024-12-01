from abc import abstractmethod
import multiprocessing
import threading
import time
from typing import Optional

import zmq

from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.integration_manager import IntegrationManager
from digitalpy.core.zmanager.subject import Subject
from digitalpy.core.zmanager.domain.model.zmanager_configuration import ZManagerConfiguration
from digitalpy.testing.facade_utilities import \
    initialize_test_environment

class ZManagerSetup:

    def __init__(self, workers: int, worker_class: str):

        self.workers = workers
        self.worker_class = worker_class
        self.zmanager_configuration: ZManagerConfiguration = SingletonConfigurationFactory.get_configuration_object("ZManagerConfiguration")

        self.zmanager_configuration.worker_count = workers

        ObjectFactory.get_instance("Configuration").set_value(
            "__class",
            worker_class,
            "RoutingWorker",
        )

        self.integration_manager = self.get_integration_manager()
        self.subject = self.get_subject()
        self.integration_manager_subscriber: zmq.Socket = None

        self.subject_thread: Optional[threading.Thread] = None
        self.integration_manager_thread: Optional[threading.Thread] = None
        self.context = zmq.Context()

    def create_integration_manager_subscriber(self):
        """create the integration manager subscriber"""
        subscriber = self.context.socket(zmq.SUB)
        subscriber.setsockopt(zmq.LINGER, 0)
        subscriber.connect(self.zmanager_configuration.integration_manager_pub_address)
        subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        return subscriber

    def get_integration_manager(self)->IntegrationManager:
        """get the integration manager"""
        return ObjectFactory.get_instance(
            "IntegrationManager",
            dynamic_configuration={"factory": ObjectFactory.get_instance("factory"), "configuration_factory": SingletonConfigurationFactory.get_instance()}
        )

    def get_subject(self) -> Subject:
        """get the subject"""
        return ObjectFactory.get_instance("Subject")

    def get_subject_address(self) -> str:
        """get the subject address"""
        return self.zmanager_configuration.subject_pull_address
    
    def send_integration_manager_message(self, message: bytes):
        """send a message to the integration manager"""
        sock = self.context.socket(zmq.PUSH)
        sock.setsockopt(zmq.LINGER, 0)
        sock.connect(self.zmanager_configuration.integration_manager_pull_address)
        message: zmq.MessageTracker = sock.send(message, track=True)
        time.sleep(0.2)
        sock.close()

    def send_subject_message(self, message: bytes):
        """send a message to the subject"""
        sock = self.context.socket(zmq.PUSH)
        sock.setsockopt(zmq.LINGER, 0)
        sock.connect(self.get_subject_address())
        
        message: zmq.MessageTracker = sock.send(message, track=True)
        time.sleep(0.2)
        sock.close()

    def receive_integration_manager_messages(self) -> list[bytes]:
        """receive messages from the integration manager"""
        messages = []
        while True:
            try:
                message = self.integration_manager_subscriber.recv_multipart(zmq.NOBLOCK)
                messages.append(message[0])
            except zmq.error.Again:
                break
        return messages

    def _start_sockets(self):
        """start the sockets"""
        self.integration_manager_subscriber = self.create_integration_manager_subscriber()

    def _stop_sockets(self):
        """stop the sockets"""
        self.integration_manager_subscriber.close()

    @abstractmethod
    def start(self):
        """setup the environment"""
        self._start_sockets()

    def stop(self):
        """teardown the environment"""
        self._stop_sockets()
        self.context.term()

class ZmanagerSingleThreadSetup(ZManagerSetup):
    """setup the zmanager in a single thread"""

    def start(self):
        super().start()
        integration_manager_thread = threading.Thread(target=self.integration_manager.start)
        integration_manager_thread.start()

        subject_thread = threading.Thread(target=self.subject.begin_routing)

        subject_thread.start()

        self.integration_manager_thread = integration_manager_thread
        self.subject_thread = subject_thread

        return integration_manager_thread, subject_thread

    def stop(self):
        super().stop()
        self.subject.running.clear()
        self.integration_manager.running.clear()

        self.subject_thread.join()
        self.integration_manager_thread.join()

class ZmanagerMultiProcSetup(ZManagerSetup):
    """setup the zmanager in multiple processes"""

    def start(self):
        integration_manager_thread = multiprocessing.Process(target=self.integration_manager.start)
        integration_manager_thread.start()

        subject_thread = multiprocessing.Process(target=self.subject.begin_routing)
        subject_thread.start()

        self.integration_manager_thread = integration_manager_thread
        self.subject_thread = subject_thread

        return integration_manager_thread, subject_thread

    def stop(self):
        super().stop()
        self.subject.running.clear()
        self.integration_manager.running.clear()
        
        self.subject_thread.join()
        self.integration_manager_thread.join()

def initialize_zmanager_multi_proc(workers: int, worker_class: str):
    _, _, configuration = initialize_test_environment()

    configuration.set_value("worker_count", workers, "Subject")
    configuration.set_value(
        "__class",
        worker_class,
        "RoutingWorker",
    )

    # begin the integration manager
    integration_manager: IntegrationManager = ObjectFactory.get_instance(
        "IntegrationManager"
    )

    integration_manager_thread = multiprocessing.Process(target=integration_manager.start)
    integration_manager_thread.start()

    # begin the subject
    subject: Subject = ObjectFactory.get_instance("Subject")

    subject_thread = multiprocessing.Process(target=subject.begin_routing)

    subject_thread.start()

    return integration_manager,integration_manager_thread,subject,subject_thread

def initialize_zmanager_single_thread(workers: int, worker_class: str):
    _, _, configuration = initialize_test_environment()

    configuration.set_value("worker_count", workers, "Subject")
    configuration.set_value(
        "__class",
        worker_class,
        "RoutingWorker",
    )

    # begin the integration manager
    integration_manager: IntegrationManager = ObjectFactory.get_instance(
        "IntegrationManager"
    )

    integration_manager_thread = threading.Thread(target=integration_manager.start)
    integration_manager_thread.start()

    # begin the subject
    subject: Subject = ObjectFactory.get_instance("Subject")

    subject_thread = threading.Thread(target=subject.begin_routing)

    subject_thread.start()

    return integration_manager,integration_manager_thread,subject,subject_thread
