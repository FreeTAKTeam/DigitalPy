import pytest

from tests.testing_utilities.facade_utilities import (
    initialize_facade,
    initialize_test_environment,
)

def test_discover_components():
    request, response = initialize_test_environment()

    component_management_facade = initialize_facade(
        "digitalpy.core.component_management.component_management_facade.ComponentManagement",
        request,
        response,
    )

    request.set_value("Directory", "tests/test_component_management/test_component_resources/")
    request.set_value("import_root", "digitalpy.core")
    request.set_value("client", None)
    
    component_management_facade.execute("GETComponentDiscovery")

    assert len(response.get_value("message")) == 1
    assert response.get_value("message")[0].name == "sample"

def test_pull_component():
    request, response = initialize_test_environment()

    component_management_facade = initialize_facade(
        "digitalpy.core.component_management.component_management_facade.ComponentManagement",
        request,
        response,
    )

    request.set_value("url", "http://example.com/")
    request.set_value("client", None)

    component_management_facade.execute("GETPullComponent")

    assert response.get_value("message") is not None

def test_install_component():
    request, response = initialize_test_environment()

    component_management_facade = initialize_facade(
        "digitalpy.core.component_management.component_management_facade.ComponentManagement",
        request,
        response,
    )

    request.set_value("Directory", "tests/test_component_management/test_component_resources/")
    request.set_value("import_root", "digitalpy.core")
    request.set_value("client", None)

    component_management_facade.execute("POSTInstallAllComponents")

    assert response.get_value("message") == "Success"
    assert response.get_value("status") == "Success"