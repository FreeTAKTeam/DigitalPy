class LogManager:
    
    def __init__(self):
        self.logger = None
    
    def configure(self, logger):
        """Configure the manager."""
        self.logger = logger
    
    def get_logs(self):
        """Get the logs from the manager."""
        with open(self.logger.handlers[0].baseFilename, 'r') as f:
            return f.read()
            
    def get_logger(self):
        """Get the logger with the given name"""
        return self.logger.get_logger()