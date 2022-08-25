class LogManager:
    
    def __init__(self):
        self.logger = None
    
    def configure(self, logger):
        self.logger = logger
    
    def get_logs(self):
        with open(self.logger.handlers[0].baseFilename, 'r') as f:
            return f.read()
            
    def get_logger(self):
        return self.logger.get_logger()