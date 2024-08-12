from pathlib import Path, PurePath
import pytest
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.object_factory import ObjectFactory
from tests.testing_utilities.facade_utilities import (
    initialize_facade,
    initialize_test_environment,
)

from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.files.files_facade import Files
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
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


def test_load_action_flow(file_facades: Files):
    """This test is used to test the load_action_flow method of the ActionFlowController class."""
    action_flow_controller = ActionFlowController()
    action_flow_file = str(
        PurePath(__file__).parent
        / PurePath("test_actionflow_resources", "simple_actionflow.ini")
    )
    file = file_facades.get_or_create_file(path=action_flow_file)
    action_flow_controller.create_action_flow(file)

    assert (
        SingletonConfigurationFactory.get_action_flow("actionflow1") is not None
    )
    assert (
        SingletonConfigurationFactory.get_action_flow("actionflow1").config_id
        == "actionflow1"
    )
    assert (
        len(SingletonConfigurationFactory.get_action_flow("actionflow1").actions)==3
    )

def test_load_action_flow_empty(file_facades: Files):
    """This test is used to test the load_action_flow method of the ActionFlowController class."""
    action_flow_controller = ActionFlowController()
    action_flow_file = str(
        PurePath(__file__).parent
        / PurePath("test_actionflow_resources", "empty_actionflow.ini")
    )
    file = file_facades.get_or_create_file(path=action_flow_file)
    action_flow_controller.create_action_flow(file)

    assert (
        SingletonConfigurationFactory.get_action_flow("actionflow1") is not None
    )
    assert (
        SingletonConfigurationFactory.get_action_flow("actionflow1").config_id
        == "actionflow1"
    )
    assert (
        len(SingletonConfigurationFactory.get_action_flow("actionflow1").actions)==0
    )

def test_get_next_action(file_facades: Files):
    """This test is used to test the get_next_action method of the ActionFlowController class."""
    action_flow_controller = ActionFlowController()
    action_flow_file = str(
        PurePath(__file__).parent
        / PurePath("test_actionflow_resources", "simple_actionflow.ini")
    )
    file = file_facades.get_or_create_file(path=action_flow_file)
    action_flow_controller.create_action_flow(file)

    request: Request = ObjectFactory.get_instance("Request")
    request.sender = "ExampleService"
    request.decorator = "decorator"
    request.context = "context"
    request.action = "Push"
    request.set_flow_name("actionflow1")
    next_action = action_flow_controller.get_next_action(request)

    assert next_action is not None
    assert next_action.action == "Publish"
    assert next_action.context == "context"
    assert next_action.decorator == "decorator"
    assert next_action.source == "Subject"

    next_request: Request = ObjectFactory.get_instance("Request")
    next_request.sender = next_action.source
    next_request.decorator = next_action.decorator
    next_request.context = next_action.context
    next_request.action = next_action.action
    next_request.set_flow_name("actionflow1")
    final_action = action_flow_controller.get_next_action(next_request)

    assert final_action is not None
    assert final_action.action == "DoAction"
    assert final_action.context == "context"
    assert final_action.decorator == "decorator"
    assert final_action.source == "IntegrationManager"

def test_get_next_action_final_action(file_facades: Files):
    """This test is used to test the get_next_action method when the current action is the final one."""
    action_flow_controller = ActionFlowController()
    action_flow_file = str(
        PurePath(__file__).parent
        / PurePath("test_actionflow_resources", "simple_actionflow.ini")
    )
    file = file_facades.get_or_create_file(path=action_flow_file)
    action_flow_controller.create_action_flow(file)

    request: Request = ObjectFactory.get_instance("Request")
    request.sender = "IntegrationManager"
    request.decorator = "decorator"
    request.context = "context"
    request.action = "DoAction"
    request.set_flow_name("actionflow1")
    next_action = action_flow_controller.get_next_action(request)

    assert next_action is None
