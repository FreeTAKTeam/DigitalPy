from multiprocessing import Event
from typing import Callable

from core.event_manager import EventManager


class DefaultEventManager(EventManager):
    __listeners = []

    def add_listener(self, event_name, callback: Callable):
        if event_name not in self.__listeners:
            self.__listeners[event_name] = []
        self.__listeners[event_name].append(callback)
    
    def remove_listener(self, event_name, callback: Callable):
        if event_name in self.__listeners:
            self.__listeners[event_name].remove(callback)
            
    def dispatch(self, event_name, event: Event):
        if event_name in self.__listeners:
            for callback in self.__listeners[event_name]:
                callback(event)
                if event.is_stopped():
                    break