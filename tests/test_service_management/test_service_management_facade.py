from unittest import mock
import pytest

from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.service_management_facade import ServiceManagement
from pathlib import PurePath
from tests.testing_utilities.facade_utilities import (
    initialize_facade,
    test_environment,
)

@pytest.fixture
def service_management_facade(test_environment):
    request, response, _ = test_environment

    service_management_facade = initialize_facade(
        "digitalpy.core.service_management.service_management_facade.ServiceManagement",
        request,
        response,
    )

    obj_configuration = ObjectFactory.get_instance("Configuration")
    obj_configuration.add_configuration(
        str(PurePath(__file__).parent / "sample_objects.ini")
    )

    test_base_configuration = InifileConfiguration("")
    test_base_configuration.add_configuration(
        str(PurePath(__file__).parent / "sample_configuration.ini")
    )
    SingletonConfigurationFactory.add_configuration(test_base_configuration)

    return service_management_facade

@mock.patch("digitalpy.core.service_management.digitalpy_service.Process", autospec=True)
def test_initialize_service(process_mock: mock.Mock, service_management_facade: ServiceManagement):
    """This test is used to test the initialize_service method of the ServiceManagement class.
    """
    service_management_facade.initialize_service("test.test_service")

    process_mock().start.assert_called_once()

@mock.patch("digitalpy.core.service_management.digitalpy_service.Process", autospec=True)
def test_stop_service_clean(process_mock: mock.Mock, service_management_facade: ServiceManagement):
    """
    This test is used to test the stop_service method of the ServiceManagement class.
    """
    service_management_facade.initialize_service("test.test_service")

    process_mock().is_alive.return_value = False

    service_management_facade.stop_service("test.test_service")

    process_mock().join.assert_called_once()

@mock.patch("digitalpy.core.service_management.digitalpy_service.Process", autospec=True)
def test_stop_service_forced(process_mock: mock.Mock, service_management_facade: ServiceManagement):
    """
    This test is used to test the stop_service method of the ServiceManagement class.
    """
    service_management_facade.initialize_service("test.test_service")

    process_mock().is_alive.return_value = True

    service_management_facade.stop_service("test.test_service", force=True)

    process_mock().terminate.assert_called_once()

@mock.patch("digitalpy.core.service_management.digitalpy_service.Process", autospec=True)
def test_restart_service(process_mock: mock.Mock, service_management_facade: ServiceManagement):
    """
    This test is used to test the restart_service method of the ServiceManagement class.
    """
    service_management_facade.initialize_service("test.test_service")

    service_management_facade.restart_service("test.test_service")

    process_mock().join.assert_called()
    process_mock().start.assert_called()

@mock.patch("digitalpy.core.service_management.digitalpy_service.Process", autospec=True)
def test_start_service(process_mock: mock.Mock, service_management_facade: ServiceManagement):
    """
    This test is used to test the start_service method of the ServiceManagement class.
    """
    SingletonConfigurationFactory.get_configuration_object("test.test_service").status = "STOPPED"

    service_management_facade.initialize_service("test.test_service")

    service_management_facade.start_service("test.test_service")

    process_mock().start.assert_called_once()