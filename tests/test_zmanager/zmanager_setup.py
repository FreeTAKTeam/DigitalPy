from abc import abstractmethod
import multiprocessing
import threading
from typing import Optional

import zmq

from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.integration_manager import IntegrationManager
from digitalpy.core.zmanager.subject import Subject
from digitalpy.core.zmanager.domain.model.zmanager_configuration import ZManagerConfiguration
from tests.testing_utilities.facade_utilities import \
    initialize_test_environment

class ZManagerSetup:

    def __init__(self, workers: int, worker_class: str):
        _, _, configuration = initialize_test_environment()

        self.workers = workers
        self.worker_class = worker_class
        self.zmanager_configuration: ZManagerConfiguration = SingletonConfigurationFactory.get_configuration_object("ZManagerConfiguration")

        self.zmanager_configuration.worker_count = workers

        configuration.set_value(
            "__class",
            worker_class,
            "RoutingWorker",
        )

        self.integration_manager = self.get_integration_manager()
        self.subject = self.get_subject()

        self.subject_thread: Optional[threading.Thread] = None
        self.integration_manager_thread: Optional[threading.Thread] = None
        self.context = zmq.Context()

    def get_integration_manager(self)->IntegrationManager:
        """get the integration manager"""
        return ObjectFactory.get_instance(
            "IntegrationManager"
        )

    def get_subject(self) -> Subject:
        """get the subject"""
        return ObjectFactory.get_instance("Subject")

    def get_subject_address(self) -> str:
        """get the subject address"""
        return self.subject.subject_address
    
    def _connect_to_integration_manager(self):
        """connect to the integration manager"""
        socket = self.context.socket(zmq.PUSH)
        socket.connect(self.zmanager_configuration.integration_manager_pull_address)
        return socket

    def send_integration_manager_message(self, message: str):
        """send a message to the integration manager"""
        sock = self._connect_to_integration_manager()
        sock.send_string(message)
        sock.close()

    @abstractmethod
    def start(self):
        """setup the environment"""

    def stop(self):
        """teardown the environment"""
        self.context.term()

class ZmanagerSingleThreadSetup(ZManagerSetup):
    """setup the zmanager in a single thread"""

    def start(self):
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
