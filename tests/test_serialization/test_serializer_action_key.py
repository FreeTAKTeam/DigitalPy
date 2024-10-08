from digitalpy.core.serialization.controllers.serializer_action_key import SerializerActionKey
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey
from tests.testing_utilities.facade_utilities import test_environment

def test_to_topic(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"config~decorator~source~context~action"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_topic(test_environment):
    _, _, _ = test_environment

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

def test_to_topic_no_config(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"~decorator~source~context~action"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_topic_no_config(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    topic = b"~decorator~source~context~action"
    expected_action_key = ActionKey(None, None)
    expected_action_key.decorator = "decorator"
    expected_action_key.source = "source"
    expected_action_key.context = "context"
    expected_action_key.action = "action"

    expected_result = (expected_action_key, b"")
    assert serializer.deserialize_from_topic(topic) == expected_result

def test_to_topic_no_decorator(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"config~~source~context~action"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_topic_no_decorator(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    topic = b"config~~source~context~action"
    expected_action_key = ActionKey(None, None)
    expected_action_key.config = "config"
    expected_action_key.source = "source"
    expected_action_key.context = "context"
    expected_action_key.action = "action"

    expected_result = (expected_action_key, b"")
    assert serializer.deserialize_from_topic(topic) == expected_result

def test_to_generic_topic(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"config~decorator~source~context~action"
    assert serializer.to_generic_topic(action_key) == expected_result

def test_to_generic_topic_no_config(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"~decorator~source~context~action"
    assert serializer.to_generic_topic(action_key) == expected_result

def test_to_generic_topic_no_decorator(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = "action"

    expected_result = b"config~~source~context~action"
    assert serializer.to_generic_topic(action_key) == expected_result
    
def test_deserialize_from_topic_no_context(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    topic = b"config~decorator~source~~action"
    expected_action_key = ActionKey(None, None)
    expected_action_key.config = "config"
    expected_action_key.decorator = "decorator"
    expected_action_key.source = "source"
    expected_action_key.context = ""
    expected_action_key.action = "action"

    expected_result = (expected_action_key, b"")
    assert serializer.deserialize_from_topic(topic) == expected_result

def test_to_topic_no_context(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = ""
    action_key.action = "action"

    expected_result = b"config~decorator~source~~action"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_topic_no_action(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    topic = b"config~decorator~source~context~"
    expected_action_key = ActionKey(None, None)
    expected_action_key.config = "config"
    expected_action_key.decorator = "decorator"
    expected_action_key.source = "source"
    expected_action_key.context = "context"
    expected_action_key.action = ""

    expected_result = (expected_action_key, b"")
    assert serializer.deserialize_from_topic(topic) == expected_result

def test_to_topic_no_action(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = "config"
    action_key.decorator = "decorator"
    action_key.source = "source"
    action_key.context = "context"
    action_key.action = ""

    expected_result = b"config~decorator~source~context~"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_topic_empty(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    topic = b""
    try:
        serializer.deserialize_from_topic(topic)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Invalid topic format for action key "

def test_to_topic_empty_action_key(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    action_key = ActionKey(None, None)
    action_key.config = ""
    action_key.decorator = ""
    action_key.source = ""
    action_key.context = ""
    action_key.action = ""

    expected_result = b"~~~~"
    assert serializer.to_topic(action_key) == expected_result

def test_deserialize_from_ini(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    ini_key = "sender?context@decorator?action=target"
    expected_action_key = ActionKey(None, None)
    expected_action_key.source = "sender"
    expected_action_key.context = "context"
    expected_action_key.decorator = "decorator"
    expected_action_key.action = "action"
    expected_action_key.target = "target"

    assert serializer.deserialize_from_ini(ini_key) == expected_action_key

def test_deserialize_from_ini_no_target(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    ini_key = "sender?context@decorator?action"
    expected_action_key = ActionKey(None, None)
    expected_action_key.source = "sender"
    expected_action_key.context = "context"
    expected_action_key.decorator = "decorator"
    expected_action_key.action = "action"
    expected_action_key.target = None

    assert serializer.deserialize_from_ini(ini_key) == expected_action_key

def test_deserialize_from_ini_invalid_format(test_environment):
    _, _, _ = test_environment

    serializer = SerializerActionKey()
    ini_key = "invalid_format"
    try:
        serializer.deserialize_from_ini(ini_key)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Invalid ini key format for action key invalid_format"
