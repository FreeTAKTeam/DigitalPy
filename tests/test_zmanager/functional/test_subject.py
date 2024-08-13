"""Test the subject functionality of the zmanager"""

import time

import pytest
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from pathlib import PurePath
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

    time.sleep(2)

    yield zmanager_setup

    zmanager_setup.stop()

def test_subject_send_to_integration_manager_action(
    zmanager: ZmanagerSingleThreadSetup,
):
    """Test that the subject can receive a request and correctly determine
    it's action is to send to a worker"""

    # build request
    request: Request = ObjectFactory.get_new_instance("Request")
    flow = SingletonConfigurationFactory.get_action_flow("testSubject1")
    request.action_key = flow.actions[0]

    request.set_value("test", "test")

    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )

    message = serializer_container.to_zmanager_message(request)

    zmanager.send_subject_message(message)

    time.sleep(1.5)

    messages = zmanager.receive_integration_manager_messages()

    assert len(messages) == 1

    received_request: Request = serializer_container.from_zmanager_message(messages[0])
    assert received_request.get_value("test") == "test"
    assert received_request.action_key == flow.actions[0]


def test_subject_send_to_worker_action(
    zmanager: ZmanagerSingleThreadSetup,
):
    """Test that the subject can receive a request and correctly determine
    it's action is to send to a worker"""

    # build request
    request: Request = ObjectFactory.get_new_instance("Request")
    flow = SingletonConfigurationFactory.get_action_flow("testSubject2")
    request.action_key = flow.actions[1]

    request.set_value("test", "test")

    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )

    message = serializer_container.to_zmanager_message(request)

    zmanager.send_subject_message(message)

    time.sleep(1.5)

    messages = zmanager.receive_integration_manager_messages()

    assert len(messages) == 1

    received_request: Request = serializer_container.from_zmanager_message(messages[0])

    assert received_request.get_value("test") == "testData"
