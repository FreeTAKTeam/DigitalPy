from digitalpy.core.serialization.controllers.serializer_action_key import SerializerActionKey
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from tests.testing_utilities.facade_utilities import initialize_test_environment

def test_to_topic():
    _, _, _ = initialize_test_environment()

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"config~decorator~source~context~action"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_topic():
    _, _, _ = initialize_test_environment()

    serializer = SerializerActionKey()
    topic = b"config~decorator~source~context~action"
    expected_action_key = ActionKey(None, None)
    expected_action_key.config = "config"
    expected_action_key.decorator = "decorator"
    expected_action_key.source = "source"
    expected_action_key.context = "context"
    expected_action_key.action = "action"

    expected_result = (expected_action_key, b"")
    assert serializer.deserialize_from_topic(topic) == expected_result

def test_to_topic_no_config():
    _, _, _ = initialize_test_environment()

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"~decorator~source~context~action"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_topic_no_config():
    _, _, _ = initialize_test_environment()

    serializer = SerializerActionKey()
    topic = b"~decorator~source~context~action"
    expected_action_key = ActionKey(None, None)
    expected_action_key.decorator = "decorator"
    expected_action_key.source = "source"
    expected_action_key.context = "context"
    expected_action_key.action = "action"

    expected_result = (expected_action_key, b"")
    assert serializer.deserialize_from_topic(topic) == expected_result

def test_to_topic_no_decorator():
    _, _, _ = initialize_test_environment()

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"config~~source~context~action"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_topic_no_decorator():
    _, _, _ = initialize_test_environment()

    serializer = SerializerActionKey()
    topic = b"config~~source~context~action"
    expected_action_key = ActionKey(None, None)
    expected_action_key.config = "config"
    expected_action_key.source = "source"
    expected_action_key.context = "context"
    expected_action_key.action = "action"

    expected_result = (expected_action_key, b"")
    assert serializer.deserialize_from_topic(topic) == expected_result
    def test_to_generic_topic():
        _, _, _ = initialize_test_environment()

        serializer = SerializerActionKey()
        action_key = ActionKey(None, None)
        action_key.config = "config"
        action_key.decorator = "decorator"
        action_key.source = "source"
        action_key.context = "context"
        action_key.action = "action"

        expected_result = b"config~decorator~source~context~action"
        assert serializer.to_generic_topic(action_key) == expected_result

def test_to_generic_topic_no_config():
    _, _, _ = initialize_test_environment()

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"~decorator~source~context~action"
    assert serializer.to_generic_topic(action_key) == expected_result

def test_to_generic_topic_no_decorator():
    _, _, _ = initialize_test_environment()

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"config~~source~context~action"
    assert serializer.to_generic_topic(action_key) == expected_result
