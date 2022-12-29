from abc import ABC, abstractmethod


class Counter(ABC):
    
    @abstractmethod
    def increment(self, value):
        """increment the counter"""
