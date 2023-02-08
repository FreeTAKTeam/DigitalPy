import re
from typing import Any

from uuid import uuid4
from digitalpy.core.domain.object_id import ObjectId
from abc import abstractmethod, ABC


class PersistentObject:

    """PersistentObject defines the interface of all persistent objects. It mainly
    requires an unique identifier for each instance (ObjectId), tracking of the
    persistent state, methods for setting and getting values as well as callback
    methods for lifecycle events.
    """

    STATE_CLEAN = 0
    STATE_DIRTY = 1
    STATE_NEW = 2
    STATE_DELETED = 3

    @abstractmethod
    def get_oid(self):
        """Get the object id of the PersistentObject."""

    @abstractmethod
    def validate_value(self, name, value):
        """Check if data may be set. The method is also called, when setting a value.
        Controller may call this method before setting data and saving the object.
        Throws a ValidationException in case of invalid data."""

    @abstractmethod
    def set_state(self, state):
        """Set the state of the object to one of the STATE constants."""

    @abstractmethod
    def get_value(self, name):
        """Get the value of an attribute"""

    @abstractmethod
    def get_mapper(self):
        """Get the PersistenceMapper of the object."""

    @abstractmethod
    def set_value(self, name, value, force_set=False, track_change=True):
        """Set the value of an attribute if it exists."""

    @abstractmethod
    def get_property_names(self):
        """Get the names of all properties in the object. Properties are
        either defined by using the PersistentObject.set_property() method
        or by the PersistentMapper."""

    @abstractmethod
    def set_property(self, name, value):
        """Set the value of a named property in the object."""

    @abstractmethod
    def validate_property(self, name, property, property_type=None):
        return self.validate_property_against_restrictions(
            name, property, property_type
        )

    @abstractmethod
    def validate_property_against_restrictions(
        self, name, property, property_type=None
    ):
        property_values = self.get_property_values(name, property_type)
        restrictions_match = property_values["restrictions_match"]
        restrictions_not_match = property_values["restrictions_not_match"]
        if (
            restrictions_match == None
            or re.match("/" + restrictions_match + "/m", property)
        ) and (
            restrictions_not_match == None
            or not re.match("/" + restrictions_not_match + "/m", property)
        ):
            return ""
        else:
            return "restrictions not met"

    @abstractmethod
    def get_property_values(self, name, property_type=None):
        if property_type is not None:
            if self._properties[property_type][name]["values"]:
                return self._properties[property_type][name]["values"]
            else:
                return None
        else:
            for property_type_dict in self._properties.values():
                if property_type_dict[name]["values"]:
                    return property_type_dict[name]["values"]
        return None

    @abstractmethod
    def after_create(self) -> Any:
        """_this method is called once after creation of this object. _at this time it is
        not known in the store.
        """

    @abstractmethod
    def after_delete(self) -> Any:
        """_this method is called once after deleting the object from the store."""

    @abstractmethod
    def after_insert(self) -> Any:
        """_this method is called once after inserting the newly created object into the
        store.
        """

    @abstractmethod
    def after_load(self) -> Any:
        """_this method is called always after loading the object from the store."""

    @abstractmethod
    def after_update(self) -> Any:
        """_this method is called always after updating the modified object in the store."""

    @abstractmethod
    def before_delete(self) -> Any:
        """_this method is called once before deleting the object from the store."""

    @abstractmethod
    def before_insert(self) -> Any:
        """_this method is called once before inserting the newly created object into the
        store.
        """

    @abstractmethod
    def before_update(self) -> Any:
        """_this method is called always before updating the modified object in the store."""

    @abstractmethod
    def clear_values(self) -> Any:
        """_clear all values. _set each value to null except for the primary key values"""

    @abstractmethod
    def copy_values(self, object: '__class__', copy_pk_values: Any = True) -> Any:
        """_copy all non-empty values to a given instance (_change_listeners are triggered)
        @param $object PersistentObject instance to copy the values to.
        @param $copy_pk_values _boolean whether primary key values should be copied
        """

    @abstractmethod
    def delete(self) -> Any:
        """_delete the object"""

    @abstractmethod
    def dump(self) -> Any:
        """_get a string representation of the values of the PersistentObject.
        @return _string
        """

    @abstractmethod
    def get_changed_values(self) -> Any:
        """_get the list of changed attributes since creation, loading.
        @return _array of value names
        """

    def get_display_value(self) -> Any:
        """_get the value of the object used for display.
        @return _the value.
        """

    @abstractmethod
    def get_indispensable_objects(self) -> Any:
        """_get the list of objects that must exist in the store, before this object may be
        persisted. _implementing classes may use this method to manage dependencies.
           @return _array of PersistentObject instances
        """

    @abstractmethod
    def get_OID(self) -> Any:
        """_get the object id of the PersistentObject.
        @return ObjectId
        """

    @abstractmethod
    def get_original_value(self, name: Any) -> Any:
        """_get the original of an attribute provided to the initialize method.
        @param $name _the name of the attribute.
        @return _the value of the attribute / null if it doesn't exist.
        """

    @abstractmethod
    def get_property(self, name: Any) -> Any:
        """_get the value of a named property in the object.
        @param $name _the name of the property.
        @return _the value of the property / null if it doesn't exist.
        """
        
    @abstractmethod
    def get_state(self) -> Any:
        """_get the object's state:
        @return _one of the STATE constant values:
        """

    @abstractmethod
    def get_type(self) -> Any:
        """_get the type of the object.
        @return _the objects type.
        """

    @abstractmethod
    def get_value_names(self, exclude_transient: Any = False) -> Any:
        """_get the names of all attributes.
           @param $exclude_transient _boolean whether to exclude transient values
        (default: _False_)
           @return _an array of attribute names.
        """

    @abstractmethod
    def get_value_property(self, name: Any, property: Any) -> Any:
        """_get the value of one property of an attribute.
        @param $name _the name of the attribute to get its properties.
        @param $property _the name of the property to get.
        @return _the value property/null if not found.
        """

    @abstractmethod
    def get_value_property_names(self, name: Any) -> Any:
        """_get the names of all properties of a value in the object.
        @return _an array consisting of the names.
        """

    @abstractmethod
    def has_value(self, name: Any) -> Any:
        """_check if the object has a given attribute.
        @param $name _the name of the attribute.
        @return _boolean whether the attribute exists or not.
        """

    @abstractmethod
    def merge_values(self, object: '__class__') -> Any:
        """_copy all values, that don't exist yet from a given instance (_change_listeners
        are not triggered)
           @param $object PersistentObject instance to copy the values from.
        """

    @abstractmethod
    def remove_value(self, name: Any) -> Any:
        """_remove an attribute.
        @param $name _the name of the attribute to remove.
        """

    @abstractmethod
    def reset(self) -> Any:
        """_reset all values to their original values"""

    @abstractmethod
    def set_oid(self, oid: ObjectId) -> Any:
        """_set the object id of the PersistentObject.
        @param $oid _the PersistentObject's oid.
        """

    @abstractmethod
    def set_value_property(self, name: Any, property: Any, value: Any) -> Any:
        """_set the value of one property of an attribute.
        @param $name _the name of the attribute to set its properties.
        @param $property _the name of the property to set.
        @param $value _the value to set on the property.
        """

    @abstractmethod
    def validate_values(self) -> Any:
        """_validate all values by calling PersistentObject::validate_value() _throws a
        _validation_exception in case of invalid data.
        """
