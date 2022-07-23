from abc import ABC

class Event(ABC):
    _is_stopped = False

    def stop_propagation(self):
        self._is_stopped = True

    def is_stopped(self):
        return self._is_stopped
        