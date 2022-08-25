from abc import ABC

class Logger(ABC):
    def debug(self, message):
        raise NotImplementedError
        
    def info(self, message):
        raise NotImplementedError
        
    def warn(self, message):
        raise NotImplementedError
        
    def error(self, message):
        raise NotImplementedError
        
    def fatal(self, message):
        raise NotImplementedError
    
    def get_logger(self, name):
        raise NotImplementedError