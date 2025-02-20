import pytest
from unittest import mock
from unittest.mock import MagicMock
from digitalpy.core.domain.domain.network_client import NetworkClient
import os
import json
from digitalpy.testing.facade_utilities import (
    initialize_facade,
    test_environment,
)

@pytest.fixture
def client_mock():
    return MagicMock(spec=NetworkClient)

@pytest.fixture
def filmology_management_db_mock():
    db_mock = mock.patch(
        "filmology_app.components.FilmologyManagement.controllers.FilmologyManagement_persistence_controller.DB_PATH",
        "sqlite:///filmology_management.db",
    )
    db_mock.start()

    yield db_mock

    db_mock.stop()
    if os.path.exists("filmology_management.db"):
        os.remove("filmology_management.db")

@pytest.mark.usefixtures("filmology_management_db_mock")
def test_post_director(client_mock, test_environment):
    request, response, _ = test_environment

    filmology_management_facade = initialize_facade(
        "filmology_app.components.FilmologyManagement.FilmologyManagement",
        request,
        response,
    )

    request.set_value("client", client_mock)

    request.set_value("body", json.dumps({
        "creator": "John Doe",
        "nationality": "American",
        "surname": "Doe",
        "created": "2023-01-01",
        "last_editor": "Jane Smith",
        "name": "John",
        "birth": "1970-01-01",
        "description": "A well-known director",
        "modified": "2023-01-02"
    }))

    filmology_management_facade.execute("POSTDirector")

    assert len(response.get_value("message")) == 1
    #assert response.get_value("message")[0] == "Director added successfully"