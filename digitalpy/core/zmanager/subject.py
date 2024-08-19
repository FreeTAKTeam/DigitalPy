import logging
import multiprocessing
import sys
from typing import TYPE_CHECKING
import zmq

from digitalpy.core.zmanager.request import Request
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
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
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )
        self.action_flow_controller: "ActionFlowController" = (
            ObjectFactory.get_instance("ActionFlowController")
        )
        self.serializer_container: SerializerContainer = ObjectFactory.get_instance(
            "SerializerContainer"
        )

    def _start_workers(self):
        for _ in range(self.zmanager_configuration.worker_count):
            worker_process = multiprocessing.Process(
                target=self.worker.start,
                daemon=True,
                args=(
                    ObjectFactory.get_instance("factory"),
                    SingletonConfigurationFactory.get_instance(),
                ),
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
        # set the timeout for the frontend pull socket so that the subject can
        # check if it should stop periodically
        self.frontend_pull.setsockopt(
            zmq.RCVTIMEO, self.zmanager_configuration.subject_pull_timeout
        )
        self.frontend_pull.setsockopt(zmq.LINGER, 0)

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
        self.worker_push.setsockopt(zmq.LINGER, 0)
        self.worker_push.setsockopt(zmq.SNDTIMEO, self.zmanager_configuration.subject_push_timeout)

    def _initialize_integration_manager_pusher(self):
        self.integration_manager_push = self.context.socket(zmq.PUSH)
        self.integration_manager_push.setsockopt(zmq.LINGER, 0)
        self.integration_manager_push.connect(
            self.zmanager_configuration.integration_manager_pull_address
        )

    def cleanup(self):
        for worker in self.workers:
            worker.terminate()
        self.worker_push.close()
        self.frontend_pull.close()
        self.integration_manager_push.close()
        self.context.term()

    def begin_routing(self):
        """Start the subject and begin routing messages."""
        self._start_workers()
        self._initiate_sockets()

        while self.running.is_set():
            try:
                message = self.frontend_pull.recv_multipart()
                self._forward_message(message)
            except zmq.error.Again:
                pass
            except Exception as ex:
                self.logger.fatal("exception thrown in subject %s", ex, exc_info=True)
        self.cleanup()
        sys.exit(0)

    def _forward_message(self, message: list[bytes]):
        """Forward the message to the appropriate destination. This involves determining
        the action key and the flow of the message. Based on this, the next action is
        determined and the message is sent to either the integration manager or the worker.
        """
        request = self._determine_next_action(message)
        if request.decorator == PUBLISH_DECORATOR:
            self.integration_manager_push.send_multipart(
                [self.serializer_container.to_zmanager_message(request)], copy=False
            )
        else:
            self.worker_push.send_multipart(
                [self.serializer_container.to_zmanager_message(request)], copy=False
            )

    def _determine_next_action(self, message: list[bytes]) -> Request:
        request = self.serializer_container.from_zmanager_message(message[0])
        if request.action == "Push":
            next_action = self.action_flow_controller.get_next_action(request)
            request.action_key = next_action
        return request

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
