import logging
import multiprocessing
from typing import TYPE_CHECKING
import zmq

from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.configuration.zmanager_constants import PUBLISH_DECORATOR
from digitalpy.core.zmanager.domain.model.zmanager_configuration import (
    ZManagerConfiguration,
)

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.action_key_controller import (
        ActionKeyController,
    )
    from digitalpy.core.zmanager.impl.default_routing_worker import DefaultRoutingWorker


class Subject:
    """part of the Z-manager architecture Dispatches events to listeners and sends messages 
    with payloads from services, acting like a load balancer. Uses a ZMQ_PUSH socket to 
    send messages to workers or to the integration manager to ewnable communication with the
    other core components.
    """

    frontend_pull: zmq.Socket

    worker_push: zmq.Socket

    integration_manager_push: zmq.Socket

    context: zmq.Context

    def __init__(
        self,
        routing_worker,
    ):
        self.workers: list[multiprocessing.Process] = []
        self.worker: "DefaultRoutingWorker" = routing_worker
        self.logger = logging.getLogger("DP-Subject_DEBUG")
        self.running = multiprocessing.Event()
        self.running.set()
        self.zmanager_configuration: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object("ZManagerConfiguration")
        )
        self.action_key_controller: "ActionKeyController" = ObjectFactory.get_instance(
            "ActionKeyController"
        )

    def _start_workers(self):
        for _ in range(self.zmanager_configuration.worker_count):
            worker_process = multiprocessing.Process(
                target=self.worker.start, daemon=True
            )
            worker_process.start()
            self.workers.append(worker_process)

    def _initiate_sockets(self):
        self.context = zmq.Context()
        self._initialize_worker_pusher()
        self._initialize_frontend_puller()
        self._initialize_integration_manager_pusher()

    def _initialize_frontend_puller(self):
        self.frontend_pull = self.context.socket(zmq.PULL)
        self.frontend_pull.bind(self.zmanager_configuration.subject_pull_address)
        # set the timeout for the frontend pull socket so that the subject can check if it should stop periodically
        self.frontend_pull.setsockopt(
            zmq.RCVTIMEO, self.zmanager_configuration.subject_pull_timeout
        )

    def _initialize_worker_pusher(self):
        self.worker_push = self.context.socket(zmq.PUSH)
        self.worker_push.bind(self.zmanager_configuration.subject_push_address)
        self.worker_push.setsockopt(
            zmq.HEARTBEAT_IVL, self.zmanager_configuration.subject_push_heartbeat_ivl
        )
        self.worker_push.setsockopt(
            zmq.HEARTBEAT_TIMEOUT,
            self.zmanager_configuration.subject_push_heartbeat_timeout,
        )
        self.worker_push.setsockopt(
            zmq.HEARTBEAT_TTL, self.zmanager_configuration.subject_push_heartbeat_ttl
        )

    def _initialize_integration_manager_pusher(self):
        self.integration_manager_push = self.context.socket(zmq.PUSH)
        self.integration_manager_push.connect(
            self.zmanager_configuration.integration_manager_pull_address
        )

    def cleanup(self):
        for worker in self.workers:
            worker.terminate()
        self.worker_push.close()
        self.frontend_pull.close()
        self.context.term()

    def begin_routing(self):
        """Start the subject and begin routing messages."""
        self._start_workers()
        self._initiate_sockets()

        while self.running.is_set():
            try:
                message = self.frontend_pull.recv_multipart()
                self.logger.debug("receieved %s", str(message))
                self._forward_message(message)
            except zmq.error.Again:
                pass
            except Exception as ex:
                self.logger.fatal("exception thrown in subject %s", ex, exc_info=True)
        self.cleanup()

    def _forward_message(self, message: list[bytes]):
        ak = self._determine_action_key(message)
        if ak.decorator == PUBLISH_DECORATOR:
            self.integration_manager_push.send_multipart(message, copy=False)
        else:
            self.worker_push.send_multipart(message, copy=False)

    def _determine_action_key(self, message: list[bytes]) -> ActionKey:
        return self.action_key_controller.deserialize_from_topic(message[0])[0]

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
