import re

from uuid import uuid4

class PersistentObject:
    def __init__(self, type) -> None:
        self._type = type
        self._id = str(uuid4())
        self._properties = {}
        self._data = {}
        self._change_listeners = []
        self._relationship_definition = {}

    def get_property_names(self, type=None):
        names = []
        if type is None:
            return self._properties.keys()
        else:
            for name in self._properties.keys():
                if self._properties[name].get_type() == type:
                    names.append(name)
            return names

    def set_property(self, name, value):
        old_value = self.get_property(name)
        self._properties[name] = value
        self.propagate_property_changes(name, old_value, value)
                
    def propagate_property_changes(self, name, old_value, value):
        for change_listener in self._change_listeners:
            if hasattr(change_listener, 'property_changed'):
                change_listener.property_changed(self, name, old_value, value)

    def validate_property(self, name, property, property_type=None):
        return self.validate_property_against_restrictions(name, property, property_type)
    
    def validate_property_against_restrictions(self, name, property, property_type=None):
        property_values = self.get_property_values(name,
                                property_type)
        restrictions_match = property_values['restrictions_match']
        restrictions_not_match = property_values['restrictions_not_match']
        if (restrictions_match == None or re.match("/"+restrictions_match+"/m", property)) \
            and (restrictions_not_match == None or not re.match("/"+restrictions_not_match+"/m", property)):
            return ''
        else:
            return 'restrictions not met'

    def get_property(self, name, type=None):
        if type is not None:
            if isinstance(self._data[type], dict) and self._data[type][name]:
                return self._data[type][name]['property']
            else:
                return None
        else:
            for cur_data_dict in self._data:
                if cur_data_dict[name]:
                    return cur_data_dict[name]['property']
        return None
        
    def get_property_values(self, name, property_type=None):
        if property_type is not None:
            if self._properties[property_type][name]['values']:
                return self._properties[property_type][name]['values']
            else:
                return None
        else:
            for property_type_dict in self._properties.values():
                if property_type_dict[name]['values']:
                    return property_type_dict[name]['values']
        return None

    def get_id(self):
        return self._id

    def get_type(self):
        return self._type
