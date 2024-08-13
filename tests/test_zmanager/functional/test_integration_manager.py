from pathlib import PurePath
import time

import pytest

from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from digitalpy.core.zmanager.configuration.zmanager_constants import RESPONSE
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.files.files_facade import Files
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from tests.test_zmanager.zmanager_setup import ZmanagerSingleThreadSetup
from tests.testing_utilities.facade_utilities import (
    initialize_facade,
    initialize_test_environment,
)


@pytest.fixture
def file_facades():
    request, response, _ = initialize_test_environment()

    files_facade: Files = initialize_facade(
        "digitalpy.core.files.files_facade.Files",
        request,
        response,
    )

    return files_facade


@pytest.fixture
def zmanager(file_facades: Files):
    _, _, _ = initialize_test_environment()

    action_flow_controller = ActionFlowController()
    action_flow_file = str(
        PurePath(__file__).parent.parent / PurePath("conf", "flows.ini")
    )
    file = file_facades.get_or_create_file(path=action_flow_file)

    action_flow_controller.create_action_flow(file)

    zmanager_setup = ZmanagerSingleThreadSetup(
        workers=1,
        worker_class="tests.test_zmanager.zmanager_test_worker.TestRoutingWorker",
    )

    zmanager_setup.start()

    time.sleep(1)

    yield zmanager_setup

    zmanager_setup.stop()


def test_integration_manager_response(zmanager: ZmanagerSingleThreadSetup):
    """Test that the integration manager can detect a completed flow and send a response"""
    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )
    request: Request = ObjectFactory.get_instance("Request")
    flow = SingletonConfigurationFactory.get_action_flow("testIntegrationManager1")
    request.action_key = flow.actions[0]
    request.set_value("test", "test")

    zmanager.send_integration_manager_message(
        serializer_container.to_zmanager_message(request)
    )
    time.sleep(2)
    response_bytes = zmanager.receive_integration_manager_messages()[0]

    resp = serializer_container.from_zmanager_response(response_bytes)
    assert resp.get_value("test") == "test"
    assert resp.action_key.config == RESPONSE


def test_integration_manager_publish(zmanager: ZmanagerSingleThreadSetup):
    """Test that the integration manager can detect a completed flow and publish a message"""
    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )
    request: Request = ObjectFactory.get_instance("Request")
    flow = SingletonConfigurationFactory.get_action_flow("testIntegrationManager2")
    request.action_key = flow.actions[0]
    request.set_value("test", "test")

    zmanager.send_integration_manager_message(
        serializer_container.to_zmanager_message(request)
    )
    time.sleep(2)
    response_bytes = zmanager.receive_integration_manager_messages()[0]

    resp = serializer_container.from_zmanager_message(response_bytes)
    assert resp.get_value("test") == "test"
    assert resp.action_key.config == "testIntegrationManager2"
    assert resp.action == "Publish"

def test_integration_manager_publish_noflow(zmanager: ZmanagerSingleThreadSetup):
    """Test that the integration manager can detect a completed flow and publish a message"""
    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )
    request: Request = ObjectFactory.get_instance("Request")
    request.action_key = ActionKey(None,None)
    request.action = "someAction"
    request.set_value("test", "test")

    zmanager.send_integration_manager_message(
        serializer_container.to_zmanager_message(request)
    )
    time.sleep(2)
    response_bytes = zmanager.receive_integration_manager_messages()[0]

    resp = serializer_container.from_zmanager_message(response_bytes)
    assert resp.get_value("test") == "test"
    assert resp.action == "someAction"
