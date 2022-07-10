from event import Event
from persistent_object import PersistentObject

class ValueChangeEvent(Event):
    NAME = "ValueChangeEvent"

    def __init__(self, object: PersistentObject, name, old_value, new_value):
        self.object = object
        self.name = name
        self.old_value = old_value
        self.new_value = new_value