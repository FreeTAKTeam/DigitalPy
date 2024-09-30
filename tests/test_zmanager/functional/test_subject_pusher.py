from pathlib import PurePath
from unittest.mock import patch, Mock

import pytest

from digitalpy.core.files.files_facade import Files
from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.zmanager.impl.subject_pusher import SubjectPusher
from digitalpy.core.main.object_factory import ObjectFactory
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

    return files_facade


@pytest.fixture
def subject_pusher():
    subject_pusher: SubjectPusher = ObjectFactory.get_instance("SubjectPusher")

    subject_pusher.pusher_socket = Mock()

    return subject_pusher

@pytest.mark.skip
@patch("digitalpy.core.zmanager.impl.subject_pusher.zmq", autospec=True)
def test_subject_send_request(
    mock_zmq, file_facades: Files, subject_pusher: SubjectPusher
):
    action_flow_controller = ActionFlowController()
    action_flow_file = str(
        PurePath(__file__).parent.parent / PurePath("conf", "flows.ini")
    )
    file = file_facades.get_or_create_file(path=action_flow_file)

    action_flow_controller.create_action_flow(file)

    # build request
    request: Request = ObjectFactory.get_new_instance("Request")
    flow = SingletonConfigurationFactory.get_action_flow("testSubject1")

    request.action_key = flow.actions[0]
    request.set_value("test", "test")
    subject_pusher.push_container(request, "TEST_SERVICE")
    subject_pusher.pusher_socket.send.assert_called_once()
