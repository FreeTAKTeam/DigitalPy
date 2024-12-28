import uuid
from datetime import datetime
from pathlib import Path

import pytest

from digitalpy.core.digipy_configuration.impl.inifile_configuration import \
    InifileConfiguration
from digitalpy.core.telemetry.domain.model.metric import Metric
from digitalpy.core.service_management.domain.model.service_status import ServiceStatus
from digitalpy.core.main.impl.status_factory import StatusFactory
from digitalpy.core.service_management.domain.model.system_event import SystemEvent
from digitalpy.core.service_management.domain.model.system_health import SystemHealth
from digitalpy.core.service_management.domain.model.system_log import SystemLog
from digitalpy.testing.facade_utilities import \
    test_environment


@pytest.fixture
def status_factory(test_environment):
    return StatusFactory()

def test_add_metric(status_factory: StatusFactory):
    metric = Metric(None, None)
    metric.metric_name = "cpu_usage"
    metric.value = 0.8
    status_factory.add_metric(metric)
    assert "cpu_usage" in status_factory.get_metrics()

def test_get_metric(status_factory: StatusFactory):
    metric = Metric(None, None)
    metric.metric_name = "cpu_usage"
    metric.value = 0.8
    status_factory.add_metric(metric)
    retrieved_metric = status_factory.get_metric("cpu_usage")
    assert retrieved_metric == metric

def test_remove_metric(status_factory: StatusFactory):
    metric = Metric(None, None)
    metric.metric_name = "cpu_usage"
    metric.value = 0.8
    status_factory.add_metric(metric)
    removed_metric = status_factory.remove_metric("cpu_usage")
    assert removed_metric == metric
    assert "cpu_usage" not in status_factory.get_metrics()

def test_add_service_status(status_factory: StatusFactory):
    service_status = ServiceStatus(None, None)
    service_status.service_name = "service_1"
    service_status.service_status = "RUNNING"
    service_status.service_status_actual = "RUNNING"
    status_factory.add_service_status(service_status)
    assert "service_1" in status_factory.get_service_statuses()

def test_get_service_status(status_factory: StatusFactory):
    service_status = ServiceStatus(None, None)
    service_status.service_name = "service_1"
    service_status.service_status = "RUNNING"
    service_status.service_status_actual = "RUNNING"
    status_factory.add_service_status(service_status)
    retrieved_service_status = status_factory.get_service_status("service_1")
    assert retrieved_service_status == service_status

def test_remove_service_status(status_factory: StatusFactory):
    service_status = ServiceStatus(None, None)
    service_status.service_name = "service_1"
    service_status.service_status = "RUNNING"
    service_status.service_status_actual = "RUNNING"
    status_factory.add_service_status(service_status)
    removed_service_status = status_factory.remove_service_status("service_1")
    assert removed_service_status == service_status
    assert "service_1" not in status_factory.get_service_statuses()

def test_add_system_event(status_factory: StatusFactory):
    system_event = SystemEvent(None, None)
    system_event.event_id = uuid.uuid4()
    system_event.message = "an event occurred"
    system_event.source = "source"
    status_factory.add_system_event(system_event)
    assert system_event in status_factory.get_system_events()

def test_set_system_health(status_factory: StatusFactory):
    system_health = SystemHealth(None, None)
    system_health.cpu = 90
    system_health.memory = 80
    system_health.disk = 70
    status_factory.set_system_health(system_health)
    assert status_factory.get_system_health() == system_health

def test_add_system_log(status_factory: StatusFactory):
    system_log = SystemLog(None, None)
    system_log.message = "Error occurred"
    system_log.timestamp = datetime.now()
    status_factory.add_system_log(system_log)
    assert system_log in status_factory.get_system_logs()

def test_clear_system_logs(status_factory: StatusFactory):
    system_log = SystemLog(None, None)
    system_log.message = "Error occurred"
    system_log.timestamp = datetime.now()
    status_factory.add_system_log(system_log)
    status_factory.clear_system_logs()
    assert status_factory.get_system_logs() == []

def test_add_configuration(status_factory: StatusFactory):
    configuration = InifileConfiguration("")
    configuration_path = Path(__file__).resolve().parent / "test_status_conf.ini"
    configuration.add_configuration(str(configuration_path))
    status_factory.add_configuration(configuration)

    assert "cpu_usage" in status_factory.get_metrics()
    assert "service_1" in status_factory.get_service_statuses()
