import pytest
from tests.testing_utilities.facade_utilities import test_environment, initialize_facade
from tests.testing_utilities.domain_utilities import (
    initialize_enum_object,
    initialize_simple_object,
    initialize_list_object,
    initialize_list_object_with_min,
    initialize_nested_object,
    initialize_nested_object_required,
    initialize_simple_list
)
from tests.testing_utilities.domain_objects import SimpleObject, ListObject, NestedObject, SimpleList, EnumObject, SimpleEnum
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
import json
from enum import Enum

def test_json_serialization_controller_simple_object(test_environment):
    request, response, _ = test_environment
    simple_obj = initialize_simple_object(request, response)
    message = json.dumps({"string": "some string data", "number": 1234})

    serialization_facade = initialize_facade("digitalpy.core.serialization.serialization_facade.Serialization", request, response)
    request.set_value("protocol", Protocols.JSON)
    request.set_value("message", message)
    request.set_value("model_object", simple_obj)
    serialization_facade.execute("desearialize_protocol_to_node")

    completed_obj: SimpleObject = response.get_value("model_object")
    assert completed_obj.string == "some string data"
    assert completed_obj.number == 1234

def test_json_serialization_controller_simple_list(test_environment):
    """Test the JSON serialization controller with an object containing a list of strings"""
    request, response, _ = test_environment
    simple_obj = initialize_simple_list(request, response)
    message = json.dumps({"string": "some string data", "number": 1234, "string_list": ["abc", "def", "hij"]})

    serialization_facade = initialize_facade(
        "digitalpy.core.serialization.serialization_facade.Serialization", 
        request,
        response
    )
    request.set_value("protocol", Protocols.JSON)
    request.set_value("message", message)
    request.set_value("model_object", simple_obj)
    serialization_facade.execute("desearialize_protocol_to_node")

    completed_obj: SimpleList = response.get_value("model_object")
    assert completed_obj.string == "some string data"
    assert completed_obj.number == 1234
    assert len(completed_obj.string_list) == 3
    assert completed_obj.string_list[0] == "abc"
    assert completed_obj.string_list[1] == "def"
    assert completed_obj.string_list[2] == "hij"

def test_json_serialization_controller_list_object_optional(test_environment):
    """Test the JSON serialization controller with an optional list object"""
    request, response, _ = test_environment
    list_obj = initialize_list_object(request, response)
    message = json.dumps({"string": "some other string", "list_data": [{"string": "abc", "number": 1}, {"string": "def", "number": 2}, {"string": "hij", "number": 3}]})

    serialization_facade = initialize_facade(
        "digitalpy.core.serialization.serialization_facade.Serialization", 
        request,
        response
    )
    request.set_value("protocol", Protocols.JSON)
    request.set_value("message", message)
    request.set_value("model_object", list_obj)
    serialization_facade.execute("desearialize_protocol_to_node")

    completed_obj: ListObject = response.get_value("model_object")
    assert completed_obj.string == "some other string"
    assert len(completed_obj.list_data) == 3
    assert completed_obj.list_data[0].string == "abc"
    assert completed_obj.list_data[0].number == 1
    assert completed_obj.list_data[1].string == "def"
    assert completed_obj.list_data[1].number == 2
    assert completed_obj.list_data[2].string == "hij"
    assert completed_obj.list_data[2].number == 3

def test_json_serialization_controller_list_object_with_minimum(test_environment):
    """Test the JSON serialization controller with an optional list object with minimum values"""
    request, response, _ = test_environment
    list_obj = initialize_list_object_with_min(request, response)
    message = json.dumps({"string": "some other string", "list_data": [{"string": "abc", "number": 1}, {"string": "def", "number": 2}, {"string": "hij", "number": 3}]})

    serialization_facade = initialize_facade(
        "digitalpy.core.serialization.serialization_facade.Serialization", 
        request,
        response
    )
    request.set_value("protocol", Protocols.JSON)
    request.set_value("message", message)
    request.set_value("model_object", list_obj)
    serialization_facade.execute("desearialize_protocol_to_node")

    completed_obj: ListObject = response.get_value("model_object")
    assert completed_obj.string == "some other string"
    assert len(completed_obj.list_data) == 3
    assert completed_obj.list_data[0].string == "abc"
    assert completed_obj.list_data[0].number == 1
    assert completed_obj.list_data[1].string == "def"
    assert completed_obj.list_data[1].number == 2
    assert completed_obj.list_data[2].string == "hij"
    assert completed_obj.list_data[2].number == 3

def test_json_serialization_controller_nested_object_optional(test_environment):
    """Test the JSON serialization controller with an optional nested object"""
    request, response, _ = test_environment
    nested_obj = initialize_nested_object(request, response)
    message = json.dumps({"string": "some other string", "nested": {"string": "abc", "number": 1}})

    serialization_facade = initialize_facade(
        "digitalpy.core.serialization.serialization_facade.Serialization", 
        request,
        response
    )
    request.set_value("protocol", Protocols.JSON)
    request.set_value("message", message)
    request.set_value("model_object", nested_obj)
    serialization_facade.execute("desearialize_protocol_to_node")

    completed_obj: NestedObject = response.get_value("model_object")
    assert completed_obj.string == "some other string"
    assert completed_obj.nested.string == "abc"
    assert completed_obj.nested.number == 1

def test_json_serialization_controller_nested_object_required(test_environment):
    """Test the JSON serialization controller with a required nested object"""
    request, response, _ = test_environment
    nested_obj = initialize_nested_object_required(request, response)
    message = json.dumps({"string": "some other string", "nested": {"string": "abc", "number": 1}})

    serialization_facade = initialize_facade(
        "digitalpy.core.serialization.serialization_facade.Serialization", 
        request,
        response
    )
    request.set_value("protocol", Protocols.JSON)
    request.set_value("message", message)
    request.set_value("model_object", nested_obj)
    serialization_facade.execute("desearialize_protocol_to_node")

    completed_obj: NestedObject = response.get_value("model_object")
    assert completed_obj.string == "some other string"
    assert completed_obj.nested.string == "abc"
    assert completed_obj.nested.number == 1

def test_json_serialization_controller_enum_object(test_environment):
    """Test the JSON serialization controller with an object containing an enumeration"""
    request, response, _ = test_environment
    enum_obj = initialize_enum_object(request, response)
    enum_obj.enum = SimpleEnum.OPTION_ONE
    enum_obj.string = "some string data"
    enum_obj.number = 1234

    serialization_facade = initialize_facade(
        "digitalpy.core.serialization.serialization_facade.Serialization", 
        request,
        response
    )
    request.set_value("protocol", Protocols.JSON)
    request.set_value("message", enum_obj)
    serialization_facade.execute("serialize_node_to_json")

    serialized_json: dict = response.get_value("message")
    assert len(serialized_json) == 1
    assert serialized_json[0]["enum"] == "a"
    assert serialized_json[0]["string"] == "some string data"
    assert serialized_json[0]["number"] == 1234