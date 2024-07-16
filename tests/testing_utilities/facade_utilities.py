import pathlib
import os
from typing import Union

from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.digipy_configuration.configuration import Configuration
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
from digitalpy.core.domain.domain.service_health import ServiceHealth
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

def initialize_test_environment() -> tuple[Request, Response]:
    """initialize the test environment
    """

    configuration = initialize_configuration()

    initialize_factory(configuration)

    # register all components
    register_components(configuration)

    # initialize the request and response objects
    request = ObjectFactory.get_new_instance("request")
    response = ObjectFactory.get_new_instance("response")
    return request, response

def initialize_factory(configuration: Configuration):
    """initialize and configure the base factory object
    """
    factory: Factory = DefaultFactory(configuration)
    ObjectFactory.configure(factory)
    return factory

def initialize_configuration() -> Configuration:
    """initialize the configuration object

    Returns:
        Configuration: initialized configuration object with the core action mapping
    """
    test_configuration: Configuration = InifileConfiguration("")
    test_configuration.add_configuration("digitalpy/core/action_mapping.ini")
    return test_configuration

def register_components(config: Configuration):
    """register all core digitalpy components
    """

    ComponentManagement(
        None, None, None, None
    ).register(config)

    Domain(
        None, None, None, None
    ).register(config)

    IAM(
        None, None, None, None
    ).register(config)

    Serialization(
        None, None, None, None
    ).register(config)

    ServiceManagement(
        None, None, None, None
    ).register(config)