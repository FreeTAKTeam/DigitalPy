import json
import os
from pathlib import PurePath
import shutil
import time
from unittest import mock
from unittest.mock import MagicMock, patch
import zipfile
import pytest

from digitalpy.core.domain.domain.network_client import NetworkClient
from tests.testing_utilities.facade_utilities import (
    initialize_facade,
    initialize_test_environment,
)


@pytest.fixture
def client_mock():
    return MagicMock(spec=NetworkClient)


@pytest.fixture(scope="session", autouse=True)
def setup():
    mock.patch(
        "digitalpy.core.component_management.controllers.component_management_persistence_controller.DB_PATH",
        "sqlite+pysqlite:///:memory:",
    ).start()

@pytest.fixture
def test_fs(zip_name: str):
    zip_path = PurePath("tests/test_component_management/test_component_resources/" + zip_name)
    content_path = PurePath("tests/test_component_management/test_component_resources/test_data")
    os.mkdir(content_path)
    with zipfile.ZipFile(zip_path, "r") as zipRef:
        zipRef.extractall(content_path)
    
    yield content_path

    shutil.rmtree(content_path)
    
@pytest.mark.parametrize("zip_name", ["test_discover_component.zip"])
def test_discover_components(client_mock, test_fs):
    mock.patch(
        "digitalpy.core.component_management.controllers.component_discovery_controller.COMPONENT_DOWNLOAD_PATH",
        PurePath(test_fs/"downloads"),
    ).start()

    request, response, _ = initialize_test_environment()

    component_management_facade = initialize_facade(
        "digitalpy.core.component_management.component_management_facade.ComponentManagement",
        request,
        response,
    )

    request.set_value("client", client_mock)

    component_management_facade.execute("GETComponentDiscovery")

    assert len(response.get_value("message")) == 1
    assert response.get_value("message")[0].name == "sample"



@patch(
    "digitalpy.core.component_management.controllers.component_pull_controller.requests.get"
)
@pytest.mark.parametrize("zip_name", ["test_pull_component.zip"])
def test_pull_component(mock_get, client_mock, test_fs):
    mock.patch(
        "digitalpy.core.component_management.controllers.component_pull_controller.COMPONENT_DOWNLOAD_PATH",
        PurePath(test_fs / "downloads"),
    ).start()

    zip_file_name = "example.zip"

    request, response, _ = initialize_test_environment()

    component_management_facade = initialize_facade(
        "digitalpy.core.component_management.component_management_facade.ComponentManagement",
        request,
        response,
    )

    mock_get.return_value.status_code = 200
    mock_get.return_value.iter_content.return_value = [b"examplezipcontent"]

    request.set_value("url", "http://example.com/" + zip_file_name)
    request.set_value("client", client_mock)

    component_management_facade.execute("GETPullComponent")

    save_path = response.get_value("message")[0]

    assert save_path.endswith(zip_file_name)

    assert os.path.exists(save_path)

    os.remove(save_path)


@pytest.mark.skip(
    "This test is not working because the component is holding the log file lock which preventst he component from being deleted once the test is complete"
)
@patch(
    "digitalpy.core.component_management.controllers.component_installation_controller.COMPONENT_DOWNLOAD_PATH",
    PurePath("tests/test_component_management/test_component_resources/"),
)
def test_install_component(client_mock):
    request, response, configuration = initialize_test_environment()

    configuration.set_value(
        "component_installation_path",
        PurePath(
            "tests\\test_component_management\\test_component_resources\\empty_test_installation_path"
        ),
        "ComponentManagement",
    )
    configuration.set_value(
        "component_import_root",
        "tsts.test_component_management.test_component_resources.empty_test_installation_path",
        "ComponentManagement",
    )
    configuration.set_value(
        "component_blueprint_path",
        PurePath(
            "tests\\test_component_management\\test_component_resources\\empty_test_blueprint_path"
        ),
        "ComponentManagement",
    )

    component_management_facade = initialize_facade(
        "digitalpy.core.component_management.component_management_facade.ComponentManagement",
        request,
        response,
    )

    request.set_value("client", client_mock)
    request.set_value("body", json.dumps({"name": "sample"}).encode("utf-8"))

    component_management_facade.execute("POSTComponent")

    component = response.get_value("message")[0]

    assert component.name == "sample"

    assert os.path.exists(
        PurePath(
            "tests\\test_component_management\\test_component_resources\\empty_test_installation_path\\sample"
        )
    )

    shutil.rmtree(
        PurePath(
            "tests\\test_component_management\\test_component_resources\\empty_test_installation_path\\sample"
        )
    )

    os.remove(
        PurePath(
            "tests\\test_component_management\\test_component_resources\\empty_test_blueprint_path\\sample_blueprint.py"
        )
    )


@pytest.mark.parametrize("zip_name", ["test_update_component.zip"])
@patch("digitalpy.core.component_management.controllers.component_management_persistence_controller_impl.Component_managementPersistenceControllerImpl.get_component")
def test_update_component(get_component_mock, client_mock, test_fs):
    mock.patch(
        "digitalpy.core.component_management.controllers.component_filesystem_controller.COMPONENT_DOWNLOAD_PATH",
        PurePath(test_fs / "downloads"),
    ).start()

    request, response, configuration = initialize_test_environment()

    configuration.set_value(
        "component_installation_path",
        PurePath(
            test_fs / "components"
        ),
        "ComponentManagement",
    )
    configuration.set_value(
        "component_import_root",
        "tests.test_component_management.test_component_resources.components",
        "ComponentManagement",
    )
    configuration.set_value(
        "component_blueprint_path",
        PurePath(
            test_fs / "blueprints"
        ),
        "ComponentManagement",
    )

    get_component_mock.return_value = [
        MagicMock(
            name="sample",
            oid=1,
            installation_path=test_fs / "components/sample",
        )
    ]

    request.set_value("client", client_mock)
    request.set_value(
        "body",
        json.dumps({"name": "sample"}).encode(
            "utf-8"
        ),
    )

    component_management_facade = initialize_facade(
        "digitalpy.core.component_management.component_management_facade.ComponentManagement",
        request,
        response,
    )

    component_management_facade.execute("PATCHComponent")

    