from abc import ABC, abstractmethod
from typing import Callable
from digitalpy.core.main.event import Event

class EventManager(ABC):
    """EventManager is responsible for dispatching events to registered listeners."""
    
    @abstractmethod
    def add_listener(self, event_name: str, callback: Callable):
        """Register a listener for a given event"""
        raise NotImplementedError

    @abstractmethod
    def remove_listener(self, event_name: str, callback: Callable):
        """Remove a listener for a given event"""
        raise NotImplementedError

    @abstractmethod
    def dispatch(self, event_name: str, event: Event):
        """Notify listeners about the given event."""
        raise NotImplementedError