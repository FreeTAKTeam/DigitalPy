import pytest
from digitalpy.core.domain.object_id import ObjectId


def test_object_id_init():
    obj_id = ObjectId("User", ["123"], "")
    assert obj_id.get_type() == "User"
    assert obj_id.get_id() == ["123"]
    assert obj_id.get_delimiter_pattern() == ":"

def test_object_id_str():
    obj_id = ObjectId("User", ["123"], "")
    assert str(obj_id) == "User:123"

def test_object_id_contains_dummy_ids():
    obj_id = ObjectId("User", ["123"], "")
    assert obj_id.contains_dummy_ids() == False

def test_object_id_is_valid():
    assert ObjectId.is_valid("User:123") == True
    assert ObjectId.is_valid("InvalidId") == False

def test_object_id_parse():
    obj_id = ObjectId.parse("User:123")
    assert obj_id.get_type() == "User"
    assert obj_id.get_id() == ["123"]

    invalid_obj_id = ObjectId.parse("InvalidId")
    assert invalid_obj_id == None
