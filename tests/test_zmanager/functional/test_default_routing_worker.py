import threading
import time
from pathlib import PurePath
from unittest import mock
from unittest.mock import patch

import pytest

from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.files.files_facade import Files
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.zmanager.configuration.zmanager_constants import (
    ZMANAGER_MESSAGE_DELIMITER,
)
from digitalpy.core.zmanager.impl.default_routing_worker import DefaultRoutingWorker
from digitalpy.core.zmanager.request import Request
from tests.test_zmanager.zmanager_setup import ZmanagerSingleThreadSetup
from tests.testing_utilities.facade_utilities import (
    initialize_facade,
    test_environment,
)


@pytest.fixture
def file_facades(test_environment):
    request, response, _ = test_environment

    files_facade: Files = initialize_facade(
        "digitalpy.core.files.files_facade.Files",
        request,
        response,
    )

    yield files_facade


@pytest.fixture
def zmanager(file_facades: Files):

    action_flow_controller = ActionFlowController()
    action_flow_file = str(
        PurePath(__file__).parent.parent / PurePath("conf", "flows.ini")
    )
    file = file_facades.get_or_create_file(path=action_flow_file)

    action_flow_controller.create_action_flow(file)

    zmanager_setup = ZmanagerSingleThreadSetup(
        workers=0,
        worker_class="digitalpy.core.zmanager.impl.default_routing_worker.DefaultRoutingWorker",
    )

    zmanager_setup.start()

    time.sleep(1)

    yield zmanager_setup

    zmanager_setup.stop()

@pytest.fixture
def default_routing_worker():
    worker: DefaultRoutingWorker = ObjectFactory.get_instance("RoutingWorker")
    worker_thread = threading.Thread(
        target=worker.start, args=(ObjectFactory.get_instance("factory"),SingletonConfigurationFactory.get_instance())
    )
    worker_thread.start()

    # wait for the worker to start
    time.sleep(0.5)

    yield worker

    worker.running.clear()
    worker_thread.join()

@patch(
    "digitalpy.core.zmanager.impl.default_routing_worker.DefaultRoutingWorker.process_integration_manager_message"
)
def test_integration_manager_subscription(
    mock_process_integration_manager_message, zmanager: ZmanagerSingleThreadSetup, default_routing_worker: DefaultRoutingWorker
):
    """Test that the default routing worker can receive messages from the integration 
    manager through the zmanager"""
    try:
        # send a message to the integration manager
        serializer_container: SerializerContainer = ObjectFactory.get_instance(
            "SerializerContainer"
        )

        request: Request = ObjectFactory.get_new_instance("Request")
        request.action_key = SingletonConfigurationFactory.get_action_flow("UPDATE_ROUTING_WORKERS").actions[0]
        message = serializer_container.to_zmanager_message(request)

        zmanager.send_integration_manager_message(message)

        time.sleep(2)

        # check that the worker received processed the message correctly
        assert mock_process_integration_manager_message.called_once
    except Exception as e:
        assert False, f"Exception occurred: {e}"

@pytest.mark.skip
def test_integration_manager_flow_request(zmanager: ZmanagerSingleThreadSetup, default_routing_worker: DefaultRoutingWorker):
    """Test that the default routing worker can send a message to the integration manager 
    through the zmanager"""
    try:
        serializer_container: SerializerContainer = ObjectFactory.get_instance(
            "SerializerContainer"
        )
        request: Request = ObjectFactory.get_instance("Request")
        flow = SingletonConfigurationFactory.get_action_flow("testWorker1")
        request.action_key = flow.actions[0]
        request.set_value("test", "test")

        default_routing_worker.action_mapper = mock.MagicMock(spec=DefaultActionMapper)

        message = serializer_container.to_zmanager_message(request)

        zmanager.send_subject_message(message)

        time.sleep(1)

        message = zmanager.receive_integration_manager_messages()[0]
        response = serializer_container.from_zmanager_response(message)

        # check that the worker received processed the message correctly
        assert response.action_key.config == "RESPONSE"
    except Exception as e:
        assert False, f"Exception occurred: {e}"
