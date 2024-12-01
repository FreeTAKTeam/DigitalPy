from unittest import mock
import pytest

from digitalpy.core.main.singleton_status_factory import SingletonStatusFactory
from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.digipy_configuration.impl.inifile_configuration import (
    InifileConfiguration,
)
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.service_management_facade import (
    ServiceManagement,
)
from pathlib import PurePath
from digitalpy.testinge_utilities import (
    initialize_facade,
    test_environment,
)


@pytest.fixture
@mock.patch(
    "digitalpy.core.zmanager.impl.integration_manager_pusher.IntegrationManagerPusher", autospec=True
)
def service_management_facade(integration_manager_pusher: mock.Mock, test_environment):
    request, response, _ = test_environment

    service_management_facade = initialize_facade(
        "digitalpy.core.service_management.service_management_facade.ServiceManagement",
        request,
        response,
        dynamic_configuration={"integration_manager_pusher": integration_manager_pusher},
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


@mock.patch(
    "digitalpy.core.service_management.controllers.service_management_process_controller.Process", autospec=True
)
def test_initialize_service(
    process_mock: mock.Mock, service_management_facade: ServiceManagement
):
    """This test is used to test the initialize_service method of the ServiceManagement class."""
    service_management_facade.initialize_service("test.test_service")

    process_mock().start.assert_called_once()


@mock.patch(
    "digitalpy.core.service_management.controllers.service_management_process_controller.Process", autospec=True
)

def test_stop_service_clean(
    process_mock: mock.Mock, service_management_facade: ServiceManagement
):
    """
    This test is used to test the stop_service method of the ServiceManagement class.
    """
    service_management_facade.initialize_service("test.test_service")

    process_mock().is_alive.return_value = False

    service_management_facade.stop_service("test.test_service")

    process_mock().join.assert_called_once()


@mock.patch(
    "digitalpy.core.service_management.controllers.service_management_process_controller.Process", autospec=True
)
def test_stop_service_forced(
    process_mock: mock.Mock, service_management_facade: ServiceManagement
):
    """
    This test is used to test the stop_service method of the ServiceManagement class.
    """
    service_management_facade.initialize_service("test.test_service")

    process_mock().is_alive.return_value = True

    service_management_facade.stop_service("test.test_service", force=True)

    process_mock().terminate.assert_called_once()


@mock.patch(
    "digitalpy.core.service_management.controllers.service_management_process_controller.Process", autospec=True
)
def test_restart_service(
    process_mock: mock.Mock, service_management_facade: ServiceManagement
):
    """
    This test is used to test the restart_service method of the ServiceManagement class.
    """
    service_management_facade.initialize_service("test.test_service")

    service_management_facade.restart_service("test.test_service")

    process_mock().join.assert_called()
    process_mock().start.assert_called()


@mock.patch(
    "digitalpy.core.service_management.controllers.service_management_process_controller.Process", autospec=True
)
def test_start_service(
    process_mock: mock.Mock, service_management_facade: ServiceManagement
):
    """
    This test is used to test the start_service method of the ServiceManagement class.
    """
    SingletonConfigurationFactory.get_configuration_object(
        "test.test_service"
    ).status = "STOPPED"

    service_management_facade.initialize_service("test.test_service")

    service_management_facade.start_service("test.test_service")

    process_mock().start.assert_called_once()


@mock.patch(
    "digitalpy.core.service_management.controllers.service_management_status_controller.psutil",
    autospec=True,
)
def test_reload_system_health(
    psutil_mock: mock.Mock, service_management_facade: ServiceManagement
):
    """
    This test is used to test the reload_system_health method of the ServiceManagement class.
    """
    psutil_mock.cpu_percent.return_value = 10
    psutil_mock.disk_usage.return_value.percent = 20
    psutil_mock.virtual_memory.return_value.percent = 30
    service_management_facade.reload_system_health()
    assert SingletonStatusFactory.get_system_health().cpu == 10
    assert SingletonStatusFactory.get_system_health().disk == 20
    assert SingletonStatusFactory.get_system_health().memory == 30


@mock.patch(
    "digitalpy.core.service_management.controllers.service_management_process_controller.Process", autospec=True
)
def test_get_service_status(_: mock.Mock, service_management_facade: ServiceManagement):
    """
    This test is used to test the get_service_status method of the ServiceManagement class.
    """
    service_management_facade.initialize_service("test.test_service")
    service_management_facade.get_service_status("test.test_service")
    assert (
        SingletonStatusFactory.get_service_status("test.test_service").service_status
        == ServiceStatusEnum.RUNNING
    )
    assert (
        SingletonStatusFactory.get_service_status("test.test_service").service_name
        == "test.test_service"
    )
    assert (
        SingletonStatusFactory.get_service_status(
            "test.test_service"
        ).service_status_actual
        == ServiceStatusEnum.RUNNING
    )
    assert (
        SingletonStatusFactory.get_service_status("test.test_service").last_error
        is None
    )
