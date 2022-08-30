from digitalpy.core.event import Event
from digitalpy.model.persistent_object import PersistentObject

class PropertyChangeEvent(Event):
    NAME = "PropertyChangeEvent"
    
    def __init__(self, object, name, old_value, new_value):
        self.object = object
        self.name = name
        self.old_value = old_value
        self.new_value = new_value
        
    def get_object(self) -> PersistentObject:
        """Get the object whose property has changed."""
        return self.object
    
    def get_property_name(self) -> str:
        """Get the name of the property that has changed."""
        return self.name
    
    def get_old_value(self):
        """get the old value"""
        return self.old_value
    
    def get_new_value(self):
        """get the new value"""
        return self.new_value