from abc import abstractmethod, ABC


class Factory(ABC):
    
    @abstractmethod
    def get_instance(self, name, dynamic_configuration={}) -> object:
        """Get an instance from the configuration. Instances created with this method
        might be shared (depending on the __shared configuration property)."""
    
    @abstractmethod
    def get_new_instance(self, name, dynamic_configuration={}) -> object:    
        """Get a new instance from the configuration. Instances created with this method are not shared."""
        
    @abstractmethod
    def get_instance_of(self, class_name, dynamic_configuration) -> object:
        """Create an instance of a class. Instances created with this method are not shared."""
        
    @abstractmethod
    def register_instance(self, name, instnce):
        """Register a shared instance with a given name."""
        
    @abstractmethod
    def add_interfaces(self, interfaces: dict):
        """Add interfaces that instances must implement."""
    
    @abstractmethod
    def clear(self):
        """Delete all created instances"""

    @abstractmethod
    def clear_instance(self, name):
        """Delete a specific instance"""