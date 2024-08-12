from digitalpy.core.zmanager.request import Request
from digitalpy.core.serialization.controllers.serializer_container import (
    SerializerContainer,
)
from digitalpy.core.main.object_factory import ObjectFactory
from tests.testing_utilities.facade_utilities import initialize_test_environment


def test_serializer_container_decorator_and_flow():
    """This test is used to test the SerializerContainer class with all optional values."""
    _, _, _ = initialize_test_environment()

    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )

    request: Request = ObjectFactory.get_new_instance("Request")

    request.action = "testAction"
    request.decorator = "testDecorator"
    request.context = "testContext"
    request.flow_name = "testFlowName"
    request.set_value("test", "test")

    serialized_message = serializer_container.to_zmanager_message(request)

    assert isinstance(serialized_message, bytes)

    deserialized_request = serializer_container.from_zmanager_message(
        serialized_message
    )

    assert deserialized_request.action == request.action
    assert deserialized_request.decorator == request.decorator
    assert deserialized_request.context == request.context
    assert deserialized_request.flow_name == request.flow_name
    assert deserialized_request.get_value("test") == "test"
    assert deserialized_request != request


def test_serializer_container_decorator():
    """This test is used to test the SerializerContainer class with decorator and now flow_name."""
    _, _, _ = initialize_test_environment()

    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )

    request: Request = ObjectFactory.get_new_instance("Request")

    request.action = "testAction"
    request.decorator = "testDecorator"
    request.context = "testContext"
    request.set_value("test", "test")

    serialized_message = serializer_container.to_zmanager_message(request)

    assert isinstance(serialized_message, bytes)

    deserialized_request = serializer_container.from_zmanager_message(
        serialized_message
    )

    assert deserialized_request.action == request.action
    assert deserialized_request.decorator == request.decorator
    assert deserialized_request.context == request.context
    assert deserialized_request.flow_name == ""
    assert deserialized_request.get_value("test") == "test"
    assert deserialized_request != request


def test_serializer_container_flow():
    """This test is used to test the SerializerContainer class with flow_name and no decorator."""
    _, _, _ = initialize_test_environment()

    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )

    request: Request = ObjectFactory.get_new_instance("Request")

    request.action = "testAction"
    request.context = "testContext"
    request.flow_name = "testFlowName"
    request.set_value("test", "test")

    serialized_message = serializer_container.to_zmanager_message(request)

    assert isinstance(serialized_message, bytes)

    deserialized_request = serializer_container.from_zmanager_message(
        serialized_message
    )

    assert deserialized_request.action == request.action
    assert deserialized_request.decorator == ""
    assert deserialized_request.context == request.context
    assert deserialized_request.flow_name == request.flow_name
    assert deserialized_request.get_value("test") == "test"
    assert deserialized_request != request


def test_serializer_container_no_decorator_or_flow():
    """This test is used to test the SerializerContainer class with no decorator or flow_name."""

    _, _, _ = initialize_test_environment()

    serializer_container: SerializerContainer = ObjectFactory.get_instance(
        "SerializerContainer"
    )

    request: Request = ObjectFactory.get_new_instance("Request")

    request.action = "testAction"
    request.context = "testContext"
    request.set_value("test", "test")

    serialized_message = serializer_container.to_zmanager_message(request)

    assert isinstance(serialized_message, bytes)

    deserialized_request = serializer_container.from_zmanager_message(
        serialized_message
    )

    assert deserialized_request.action == request.action
    assert deserialized_request.decorator == ""
    assert deserialized_request.context == request.context
    assert deserialized_request.flow_name == ""
    assert deserialized_request.get_value("test") == "test"
    assert deserialized_request != request
