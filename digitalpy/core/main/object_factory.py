from digitalpy.core.main.factory import Factory
from typing import Any

class ObjectFactory:
    __factory = None

    @staticmethod
    def configure(factory: Factory):
        ObjectFactory.__factory = factory

    @staticmethod
    def is_configured():
        """Check if the factory is configured."""
        return ObjectFactory.__factory != None

    @staticmethod
    def get_instance(name, dynamic_configuration={}) -> Any:
        """Get an instance from the configuration. Instances created with this method
        might be shared (depending on the __shared configuration property)."""
        ObjectFactory.__check_config()
        return ObjectFactory.__factory.get_instance(name, dynamic_configuration)

    @staticmethod
    def get_new_instance(name, dynamic_configuration={}) -> Any:
        """Get a new instance from the configuration. Instances created with this method are not shared."""
        ObjectFactory.__check_config()
        return ObjectFactory.__factory.get_new_instance(name, dynamic_configuration)

    @staticmethod
    def __check_config():
        if ObjectFactory.__factory is None:
            raise Exception(
                "No Factory instance provided. Do this by calling the configure() method."
            )

    @staticmethod
    def get_instance_of(class_name, dynamic_configuration={}):
        """Create an instance of a class. Instances created with this method are not shared."""
        ObjectFactory.__check_config()
        return ObjectFactory.__factory.get_instance_of(
            class_name, dynamic_configuration
        )

    def add_interfaces(self, interfaces):
        """Add interfaces that instances must implement."""
        ObjectFactory.__check_config()
        ObjectFactory.__factory.add_interfaces(interfaces)

    @staticmethod
    def clear():
        """clear the configured factory instance"""
        if ObjectFactory.__factory != None:
            ObjectFactory.__factory.clear()
        ObjectFactory.__factory = None

    @staticmethod
    def register_instance(name, instance):
        """Register a shared instance with a given name."""
        ObjectFactory.__check_config()
        ObjectFactory.__factory.register_instance(name, instance)
