from digitalpy.core.persistence.impl.null_mapper import NullMapper
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.persistence.persistent_object import PersistentObject
from digitalpy.core.persistence.property_change_event import PropertyChangeEvent
from digitalpy.core.persistence.value_change_event import ValueChangeEvent


class DefaultPersistentObject(PersistentObject):
    id = None
    __type = ""
    data = {}
    properties = {}
    value_properties = {}
    state = PersistentObject.STATE_CLEAN
    changed_attributes = {}
    original_data = {}
    mapper = None

    null_mapper = None

    def __init__(self, oid: ObjectId = None, initial_data=None):
        if oid is None or not ObjectId.is_valid(oid):
            oid = ObjectId.NULL_OID()
        self.__type = oid.get_type()
        self._oid = oid
        if oid.contains_dummy_ids():
            self.state = DefaultPersistentObject.STATE_NEW
        else:
            self.state = DefaultPersistentObject.STATE_CLEAN

        data = {}
        self.attribute_descriptions = self.get_mapper().get_attributes()
        for cur_attribute_desc in self.attribute_descriptions:
            data[cur_attribute_desc.get_name()] = cur_attribute_desc.get_default_value()

        if initial_data is not None:
            data = {**data, **initial_data}

        for name, value in data.items():
            self.set_value_internal(name, value)

        self.original_data = data

        self._set_oid_internal(oid, False)

    def __initialize_mapper(self):
        self.persistence_facade = ObjectFactory.get_instance("persistencefacade")
        if self.persistence_facade.is_known_type(self.__type):
            self.mapper = self.persistence_facade.get_mapper(self.__type)
        else:
            if DefaultPersistentObject.null_mapper == None:
                DefaultPersistentObject.null_mapper = NullMapper()
            self.mapper = DefaultPersistentObject.null_mapper

    def _set_oid_internal(self, oid: ObjectId, trigger_listeners):
        self.__type = oid.get_type()
        self._oid = oid

        ids = oid.get_id()
        pk_names = self.get_mapper().get_pk_names()
        for i in range(len(pk_names)):
            if trigger_listeners:
                self.set_value(pk_names[i], ids[i], True)
            else:
                self.set_value_internal(pk_names[i], ids[i])

    def set_property(self, name, value):
        old_value = self.get_property(name)
        self._properties[name] = value
        ObjectFactory.get_instance("eventManager").dispatch(
            PropertyChangeEvent.NAME, PropertyChangeEvent(self, name, old_value, value)
        )

    def get_properties(self):
        return self.properties

    def get_property(self, name):
        if name in self.properties:
            return self.properties[name]
        else:
            properties = self.get_mapper().get_properties()
            if name in properties:
                return properties[name]

    @classmethod
    def get_value(cls, name):
        return cls.data.get(name, None)

    @classmethod
    def set_state(cls, state):
        raise NotImplementedError("this method is not implemented yet")

    def validate_value(self, name, value):
        raise NotImplementedError("this method is not implemented yet")

    def get_mapper(self):
        if self.mapper is None:
            self.__initialize_mapper()
        return self.mapper

    def set_value(self, name, value, force_set=False, track_change=True):
        if not force_set:
            self.validate_value(name, value)
        old_value = self.get_value(name)
        if force_set or old_value != value:
            self.set_value_internal(name, value)
            if name in self.get_mapper().get_pk_names():
                self.update_oid()
            if track_change:
                DefaultPersistentObject.set_state(DefaultPersistentObject.STATE_DIRTY)
                self.changed_attributes[name] = True
                ObjectFactory.get_instance("eventManager").dispatch(
                    ValueChangeEvent.NAME,
                    ValueChangeEvent(self, name, old_value, value),
                )
            return True
        return False

    def get_property_names(self):
        result = self.get_mapper().get_properties().keys()
        return result.extend(self.properties.keys())

    def set_value_internal(self, name, value):
        """Internal (fast) version to set a value without any validation, state change,
        listener notification etc."""
        self.data[name] = value

    def get_oid(self):
        return self._oid

    def get_type(self) -> str:
        """the current class name

        Returns:
            str: class name
        """
        return self.__class__.__name__