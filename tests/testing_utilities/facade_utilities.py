from typing import Union

from digitalpy.core.telemetry.singleton_status_factory import SingletonStatusFactory
from digitalpy.core.telemetry.domain.status_factory import StatusFactory
from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.main.factory import Factory
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

from digitalpy.core.component_management.component_management_facade import ComponentManagement
from digitalpy.core.domain.domain_facade import Domain
from digitalpy.core.IAM.IAM_facade import IAM
from digitalpy.core.serialization.serialization_facade import Serialization
from digitalpy.core.service_management.service_management_facade import ServiceManagement

def initialize_facade(facade_class: str, request: Request, response: Response) -> Union[DefaultFacade, Request, Response]:
    """intialize the given facade class
    NOTE: you should call the initialize test environment method first

    Args:
        facade_class (str): the name of the facade class to initialize

    Returns:
        DefaultFacade: the initialized facade
        Request: the initialized request object
        Response: the initialized response object
    """
    facade = ObjectFactory.get_instance_of(facade_class, dynamic_configuration={"request": request, "response": response})
    facade.initialize(request, response)
    return facade

def initialize_test_environment() -> tuple[Request, Response, Configuration]:
    """initialize the test environment
    """

    initialize_factorys()

    # register all components
    register_components()

    # initialize the request and response objects
    request = ObjectFactory.get_new_instance("request")
    response = ObjectFactory.get_new_instance("response")
    return request, response, ObjectFactory.get_instance("Configuration")

def initialize_factorys():
    """initialize and configure the base factory object
    """
    configuration = initialize_configuration()
    factory: Factory = DefaultFactory(configuration)
    ObjectFactory.configure(factory)

    test_base_configuration: Configuration = InifileConfiguration("")
    test_base_configuration.add_configuration("digitalpy/core/configuration_management.ini")
    conf_fact = ConfigurationFactory()
    conf_fact.add_configuration(test_base_configuration)
    SingletonConfigurationFactory.configure(conf_fact)

    test_status_configuration: Configuration = InifileConfiguration("")
    test_status_configuration.add_configuration("digitalpy/core/core_status.ini")
    status_factory = StatusFactory()
    status_factory.add_configuration(test_status_configuration)
    SingletonStatusFactory.configure(status_factory)

    return factory

def initialize_configuration() -> Configuration:
    """initialize the configuration object

    Returns:
        Configuration: initialized configuration object with the core action mapping
    """
    test_configuration: Configuration = InifileConfiguration("")
    test_configuration.add_configuration("digitalpy/core/core_config.ini")
    return test_configuration

def register_components():
    """register all core digitalpy components
    """

    register_component(ComponentManagement(None, None, None, None))

    register_component(Domain(None, None, None, None))

    register_component(IAM(None, None, None, None))

    register_component(Serialization(None, None, None, None))

    register_component(ServiceManagement(None, None, None, None))

def register_component(facade: DefaultFacade):
    """register the given component facade"""
    config: Configuration = ObjectFactory.get_instance("Configuration")
    config.add_configuration(facade.get_configuration_path())

    ObjectFactory.register_instance(
        facade.__class__.__name__.lower()+"actionmapper",
        facade.get_action_mapper(),
    )

    facade.setup()