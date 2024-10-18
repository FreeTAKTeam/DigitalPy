from typing import Union
from threading import Lock
import pathlib

import pytest

from digitalpy.core.digipy_configuration.controllers.action_flow_controller import (
    ActionFlowController,
)
from digitalpy.core.files.files_facade import Files
from digitalpy.core.main.singleton_status_factory import SingletonStatusFactory
from digitalpy.core.main.impl.status_factory import StatusFactory
from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.digipy_configuration.impl.inifile_configuration import (
    InifileConfiguration,
)
from digitalpy.core.main.factory import Factory
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

from digitalpy.core.component_management.component_management_facade import (
    ComponentManagement,
)
from digitalpy.core.domain.domain_facade import Domain
from digitalpy.core.IAM.IAM_facade import IAM
from digitalpy.core.serialization.serialization_facade import Serialization
from digitalpy.core.service_management.service_management_facade import (
    ServiceManagement,
)

def initialize_facade(
    facade_class: str, request: Request, response: Response, dynamic_configuration: dict = None
) -> Union[DefaultFacade, Request, Response]:
    """intialize the given facade class
    NOTE: you should call the initialize test environment method first

    Args:
        facade_class (str): the name of the facade class to initialize

    Returns:
        DefaultFacade: the initialized facade
        Request: the initialized request object
        Response: the initialized response object
    """
    if not dynamic_configuration:
        dynamic_configuration = {}
    facade = ObjectFactory.get_instance_of(
        facade_class, dynamic_configuration={"request": request, "response": response, **dynamic_configuration}
    )
    facade.initialize(request, response)
    return facade


def initialize_test_environment() -> tuple[Request, Response, Configuration]:
    """initialize the test environment"""
    print('initializing factorys')
    # initialize the factory object
    initialize_factorys()

    print('registering components')
    # register all components
    register_components()

    print('registering flows')
    # register flows
    register_flows()

    # initialize the request and response objects
    request = ObjectFactory.get_new_instance("request")
    response = ObjectFactory.get_new_instance("response")
    return request, response, ObjectFactory.get_instance("Configuration")


def cleanup_test_environment():
    """cleanup the test environment"""
    ObjectFactory.clear()
    SingletonConfigurationFactory.clear()
    SingletonStatusFactory.clear()

def initialize_factorys():
    """initialize and configure the base factory object"""
    configuration = initialize_configuration()
    factory: Factory = DefaultFactory(configuration)
    ObjectFactory.configure(factory)

    print("initializing configuration factory")
    test_base_configuration: Configuration = InifileConfiguration("")
    test_base_configuration.add_configuration(
        "digitalpy/core/configuration_management.ini"
    )
    conf_fact = ConfigurationFactory()
    conf_fact.add_configuration(test_base_configuration)
    print("adding configuration factory conf")
    SingletonConfigurationFactory.configure(conf_fact)

    print("initializing status factory")
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
    """register all core digitalpy components"""
    print("initializing IAM")
    register_component(IAM(None, None, None, None))
    print("initialized IAM")

    print("initializing Files")
    register_component(Files(None, None, None, None))
    print("initialized Files")

    print("initializing ComponentManagement")
    register_component(ComponentManagement(None, None, None, None))
    print("initialized ComponentManagement")

    print("initializing Domain")
    register_component(Domain(None, None, None, None))
    print("initialized Domain")

    print("initializing Serialization")
    register_component(Serialization(None, None, None, None))
    print("initialized Serialization")

    print("initializing ServiceManagement")
    register_component(ServiceManagement(None, None, None, None))
    print("initialized ServiceManagement")

def register_flows():
    action_flow_controller = ActionFlowController()
    action_flow_file = str(
        pathlib.PurePath(__file__).parent.parent.parent
        / pathlib.PurePath("digitalpy", "core", "core_flows.ini")
    )
    file_facades: Files = ObjectFactory.get_instance("Files")
    file = file_facades.get_or_create_file(path=action_flow_file)

    action_flow_controller.create_action_flow(file)


def register_component(facade: DefaultFacade):
    """register the given component facade"""
    action_mapping_conf = InifileConfiguration(facade.get_configuration_path())
    action_mapping_conf.add_configuration("")
    SingletonConfigurationFactory.add_configuration(action_mapping_conf)

    ObjectFactory.register_instance(
        facade.__class__.__name__.lower() + "actionmapper",
        facade.get_action_mapper(),
    )
    facade.setup()

@pytest.fixture(scope="function")
def test_environment():
    """initialize the test environment"""
    request, response, conf = initialize_test_environment()
    yield request, response, conf
    cleanup_test_environment()
