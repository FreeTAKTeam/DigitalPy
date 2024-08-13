import threading
import time
from unittest.mock import patch
import pytest

from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.zmanager.request import Request
from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER,
)
from digitalpy.core.zmanager.impl.default_routing_worker import DefaultRoutingWorker
from tests.test_zmanager.zmanager_setup import ZmanagerSingleThreadSetup
from tests.testing_utilities.facade_utilities import initialize_test_environment


@patch(
    "digitalpy.core.zmanager.impl.default_routing_worker.DefaultRoutingWorker.process_integration_manager_message"
)
def test_integration_manager_subscription(mock_process_integration_manager_message):
    """Test that the default routing worker can receive messages from the integration manager through the zmanager"""
    _, _, _ = initialize_test_environment()

    # setup the zmanager in a single thread with no workers
    zmanager = ZmanagerSingleThreadSetup(
        workers=0,
        worker_class="digitalpy.core.zmanager.impl.default_routing_worker.DefaultRoutingWorker",
    )
    zmanager.start()

    # start the default routing worker in a thread
    worker: DefaultRoutingWorker = ObjectFactory.get_instance("RoutingWorker")
    worker_thread = threading.Thread(target=worker.start, args=(ObjectFactory.get_instance("factory"),))
    worker_thread.start()

    # wait for the worker to start
    time.sleep(0.5)
    try:
        # send a message to the integration manager
        serializer_container: SerializerContainer = ObjectFactory.get_instance(
            "SerializerContainer"
        )

        request: Request = ObjectFactory.get_new_instance("Request")
        request.decorator = "ROUTING_WORKER"
        request.action_key.config = ""
        message = serializer_container.to_zmanager_message(request)

        # wait for the worker to process the message
        time.sleep(2)

        zmanager.send_integration_manager_message(message)

        time.sleep(1)

        # check that the worker received processed the message correctly
        assert mock_process_integration_manager_message.called
        mock_process_integration_manager_message.assert_called_with(message)
    except Exception as e:
        assert False, f"Exception occurred: {e}"

    finally:
        # stop the zmanager
        zmanager.stop()
        worker.running.clear()
        worker_thread.join()


@pytest.mark.skip(reason="This test is not working as expected")
def test_object_factory_update():
    _, _, _ = initialize_test_environment()

    # setup the zmanager in a single thread with no workers
    zmanager = ZmanagerSingleThreadSetup(
        workers=0,
        worker_class="digitalpy.core.zmanager.impl.default_routing_worker.DefaultRoutingWorker",
    )
    zmanager.start()

    # start the default routing worker in a thread
    worker: DefaultRoutingWorker = ObjectFactory.get_instance("RoutingWorker")
    worker_thread = threading.Thread(target=worker.start)
    worker_thread.start()

    # wait for the worker to start
    time.sleep(0.1)

    # send a message to the integration manager
    message_topic = b"routing_worker"
    message_content = b"content"
    message = message_topic + ZMANAGER_MESSAGE_DELIMITER + message_content
    zmanager.send_integration_manager_message(message)

    # wait for the worker to process the message
    time.sleep(0.1)

    # check that the worker received processed the message correctly
    assert worker.processed_messages == [message_content.encode()]

    # stop the zmanager
    zmanager.stop()
    worker.running.clear()
    worker_thread.join()
