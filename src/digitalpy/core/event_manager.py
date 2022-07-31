from abc import ABC

from digitalpy.core.event import Event

class EventManager(ABC):
    def add_listener(self, event_name, callback):
        raise NotImplementedError

    def remove_listener(self, event_name, callback):
        raise NotImplementedError

    def dispatch(self, event_name, event: Event):
        raise NotImplementedError