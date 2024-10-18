import zmq

from digitalpy.core.main.factory import Factory
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.domain.model.zmanager_configuration import (
    ZManagerConfiguration,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)


class TestRoutingWorker:
    """a test worker that routes messages from a subject to an integration manager without any processing"""

    def __init__(self):
        self.zmanager_conf: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )
        self.serializer_container: SerializerContainer = ObjectFactory.get_instance(
            "SerializerContainer"
        )

    def initiate_sockets(self):
        """initiate all socket connections"""
        context = zmq.Context()
        self.sock = context.socket(zmq.PULL)
        self.sock.connect(self.zmanager_conf.subject_push_address)
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.sock.setsockopt(zmq.RCVHWM, 0)
        self.integration_manager_sock = context.socket(zmq.PUSH)
        self.integration_manager_sock.connect(
            self.zmanager_conf.integration_manager_pull_address
        )
        # unlimited as trunkating can result in unsent data and broken messages
        # TODO: determine a sane default
        self.integration_manager_sock.setsockopt(zmq.SNDHWM, 0)

    def start(self, factory: Factory):
        ObjectFactory.configure(factory)
        self.initiate_sockets()
        while True:
            try:
                message = self.sock.recv_multipart().pop(0)
                request = self.serializer_container.from_zmanager_message(message)
                request.set_value("test", "testData")
                self.integration_manager_sock.send(
                    self.serializer_container.to_zmanager_message(request), copy=False
                )
            except Exception as ex:
                print(f"exception thrown in worker {ex}")
