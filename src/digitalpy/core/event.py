from abc import ABC

class Event(ABC):
    """Event is the base class for all events."""
    __is_stopped = False

    def stop_propagation(self):
        """Stop further processing of the event"""
        self.__is_stopped = True

    def is_stopped(self) -> bool:
        """Check if the event is stopped"""
        return self.__is_stopped
        