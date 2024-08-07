from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration


class SingletonConfigurationFactory:
    """ConfigurationFactory class to create and retrieve configuration objects."""

    __factory: ConfigurationFactory = None

    @staticmethod
    def configure(factory):
        """Configure the factory."""
        SingletonConfigurationFactory.__factory = factory

    @staticmethod
    def add_configuration(configuration: Configuration):
        """Get an instance from the configuration."""
        SingletonConfigurationFactory.__check_config()
        return SingletonConfigurationFactory.__factory.add_configuration(configuration)

    @staticmethod
    def remove_configuration(name: str):
        """Remove a configuration object."""
        SingletonConfigurationFactory.__check_config()
        return SingletonConfigurationFactory.__factory.remove_configuration(name)

    @staticmethod
    def get_configuration_object(name: str) -> object:
        """Get a new instance from the configuration."""
        SingletonConfigurationFactory.__check_config()
        return SingletonConfigurationFactory.__factory.get_configuration_object(name)

    @staticmethod
    def __check_config():
        if SingletonConfigurationFactory.__factory is None:
            raise Exception(
                "No Factory instance provided. Do this by calling the configure() method."
            )
