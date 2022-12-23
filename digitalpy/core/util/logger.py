from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def debug(self, message):
        """record a debug message"""

    @abstractmethod
    def info(self, message):
        """record a info message"""

    @abstractmethod
    def warn(self, message):
        """record a warn message"""

    @abstractmethod
    def error(self, message):
        """record a error message"""

    @abstractmethod
    def fatal(self, message):
        """record a fatal message"""

    @abstractmethod
    def get_logger(self, name):
        """Get a Logger instance by name"""
