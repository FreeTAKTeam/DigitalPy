from digitalpy.model.impl.null_mapper import NullMapper
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.model.object_id import ObjectId
from digitalpy.model.persistent_object import PersistentObject
from digitalpy.model.value_change_event import ValueChangeEvent


class DefaultPersistentObject(PersistentObject):
    id = None
    _type = ''
    data = {}
    properties = {}
    value_properties = {}
    state = PersistentObject.STATE_CLEAN
    changed_attributes = {}
    original_data = {}
    mapper = None

    null_mapper = None

    def __init__(self, oid: ObjectId = None, initial_data = None):
        if oid is None or not ObjectId.is_valid(oid):
            oid = ObjectId.NULL_OID()
        self.type = oid.get_type()
        self.oid = oid
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
        self.persistence_facade = ObjectFactory.get_instance('persistence_facade')
        if self.persistence_facade.is_known_type(self.type):
            self.mapper = self.persistence_facade.get_mapper(self.type)
        else:
            if DefaultPersistentObject.null_mapper == None:
                DefaultPersistentObject.null_mapper = NullMapper()
            self.mapper = DefaultPersistentObject.null_mapper

    def _set_oid_internal(self, oid: ObjectId, trigger_listeners):
        self.type = oid.get_type()
        self.oid = oid
        
        ids = oid.get_id()
        pk_names = self.get_mapper().get_pk_names()
        for i in range(pk_names):
            if trigger_listeners:
                self.set_value(pk_names[i], ids[i], True)
            else:
                self.set_value_internal(pk_names[i], ids[i])

    def get_mapper(self):
        if self.mapper is None:
            self.__initialize_mapper()
        return self.mapper
    
    def set_value(self, name, value, force_set=False, track_change=True):
        if not force_set:
            self.validate_value(name, value)
        old_value = DefaultPersistentObject.get_value(name)
        if force_set or old_value != value:
            self.set_value_internal(name, value)
            if name in self.get_mapper().get_pk_names():
                self.update_oid()
            if track_change:
                DefaultPersistentObject.setState(DefaultPersistentObject.STATE_DIRTY)
                self.changed_attributes[name] = True
                ObjectFactory.get_instance('eventManager').dispatch(ValueChangeEvent.NAME, ValueChangeEvent(self, name, old_value, value))
            return True
        return False
    
    def set_value_internal(self, name, value):
        self.data[name] = value
    
    def get_oid(self):
        return self.oid