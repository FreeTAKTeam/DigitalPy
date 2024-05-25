import pytest
from digitalpy.core.domain.relationship import Relationship, RelationshipType

class TestOneEntity:
    @Relationship()
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

class TestMultipleEntity:
    @Relationship(reltype=RelationshipType.ASSOCIATION, multiplicity_lower=1, multiplicity_upper=2)
    def names(self):
        return self._names

    @names.setter
    def names(self, value):
        self._names = value

class TestUnNavigableEntity:
    @Relationship(navigable=False)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

def test_relationship_getter_and_setter():
    entity = TestOneEntity()
    entity.name = "Test"
    assert entity.name == "Test"

def test_invalid_relationship_type():
    with pytest.raises(ValueError):
        @Relationship(reltype="invalid")
        def invalid(self):
            pass

def test_one_to_many_relationship():
    entity = TestMultipleEntity()
    entity.names = ["Test1", "Test2"]
    assert entity.names == ["Test1", "Test2"]

def test_invalid_one_to_many_relationship():
    entity = TestMultipleEntity()
    with pytest.raises(ValueError):
        entity.names = "Test"

def test_invalid_one_to_many_relationship_too_many_rels():
    entity = TestMultipleEntity()
    with pytest.raises(ValueError):
        entity.names = ["Test1", "Test2", "Test3"]

def test_invalid_one_to_many_relationship_too_few_rels():
    entity = TestMultipleEntity()
    with pytest.raises(ValueError):
        entity.names = []

def test_unnavigable_relationship():
    entity = TestUnNavigableEntity()
    entity._name = "Test"
    with pytest.raises(AttributeError):
        entity.name