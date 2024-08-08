from typing import Any, Optional
from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration


class SingletonConfigurationFactory:
    """ConfigurationFactory class to create and retrieve configuration objects."""

    __factory: Optional[ConfigurationFactory] = None

    @staticmethod
    def configure(factory):
        """Configure the factory."""
        SingletonConfigurationFactory.__factory = factory

    @staticmethod
    def add_configuration(configuration: Configuration):
        """Get an instance from the configuration."""
        SingletonConfigurationFactory.__check_config()
        return SingletonConfigurationFactory.__factory.add_configuration(configuration)  # type: ignore

    @staticmethod
    def remove_configuration(configuration: Configuration):
        """Remove a configuration object."""
        SingletonConfigurationFactory.__check_config()
        return SingletonConfigurationFactory.__factory.remove_configuration(  # type: ignore
            configuration
        )

    @staticmethod
    def get_configuration_object(name: str) -> Any:
        """Get a new instance from the configuration."""
        SingletonConfigurationFactory.__check_config()
        return SingletonConfigurationFactory.__factory.get_configuration_object(name)  # type: ignore

    @staticmethod
    def __check_config():
        if SingletonConfigurationFactory.__factory is None:
            raise Exception(
                "No Factory instance provided. Do this by calling the configure() method."
            )
