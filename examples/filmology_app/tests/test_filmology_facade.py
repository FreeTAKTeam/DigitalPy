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

    os.remove("filmology_management.db")

def seed_database(url):
    from sqlite3 import connect
    connect(url).executescript("""INSERT INTO Director (oid,creator,nationality,surname,created,last_editor,name,birth,description,modified) VALUES
	 ('Director:8721cddb-efe4-11ef-b8e9-60dd8ec76433','Michael Thompson','American','Thompson','2025-02-20','Sarah Lee','Michael','1985-08-30','A data scientist with expertise in machine learning and AI.','2025-02-22T14:45:00Z');
    INSERT INTO Actor (oid,creator,nationality,surname,created,last_editor,name,birth,description,modified,Movie_oid) VALUES
	 ('Actor:0393e0e8-efe4-11ef-875b-60dd8ec76433','Alice Johnson','Canadian','Johnson','2025-02-20','Bob Smith','Alice','1990-05-15','A software engineer specializing in backend development.','2025-02-21T10:15:30Z',NULL);
    INSERT INTO Date (oid,"year",name) VALUES
	 ('Date:c2aa3824-efdc-11ef-a8ca-60dd8ec76433','2004','bday'),
     ('Date:faa3b1b4-efdb-11ef-8b1b-60dd8ec76433','2005','new day');
    INSERT INTO Genre (oid,name) VALUES
	 ('Genre:3b053d2a-ae98-11ef-bd08-60dd8ec76433','horror'),
	 ('Genre:8304ae3b-efdd-11ef-bd39-60dd8ec76433','tragedy');
    INSERT INTO Movie (oid,date,country,creator,color,created,last_editor,runtime,description,URL,plot,name,alias,modified,CompositionPosterPrimary_oid,Date_oid) VALUES
	 ('Movie:efba28d6-efe0-11ef-b7f9-60dd8ec76433','2025-02-22','Canada','Jane Doe','#FF5733','2025-02-20','John Smith','120 minutes','This is a sample project demonstrating JSON schema usage.','https://www.example.com/sample_project','A brief overview of the project''s objectives and scope.','Sample Project','sample_project','2025-02-21T15:30:00Z','Poster:f5698d56-efdb-11ef-a458-60dd8ec76433','Date:c2aa3824-efdc-11ef-a8ca-60dd8ec76433');
    INSERT INTO Poster (oid,name) VALUES
	 ('Poster:f5698d56-efdb-11ef-a458-60dd8ec76433','a poster'),
     ('Poster:faa3b1b4-efdb-11ef-8b1b-60dd8ec76433','another poster');
""").close()

@pytest.mark.usefixtures("filmology_management_db_mock")
def test_post_director_lifecycle(client_mock, test_environment):
    request, response, _ = test_environment

    filmology_management_facade = initialize_facade(
        "filmology_app.components.FilmologyManagement.FilmologyManagement_facade.FilmologyManagement",
        request,
        response,
    )

    seed_database("filmology_management.db")

    request.set_value("client", client_mock)

    request.set_value("body", json.dumps({
        "created": "2025-02-20",
        "creator": "Michael Thompson",
        "last_editor": "Sarah Lee",
        "modified": "2025-02-22T14:45:00Z",
        "name": "Michael",
        "description": "A data scientist with expertise in machine learning and AI.",
        "surname": "Thompson",
        "birth": "1985-08-30",
        "nationality": "American",
    }).encode())

    filmology_management_facade.execute("POSTDirector")

    assert len(response.get_value("message")) == 1
    assert response.get_value("message")[0].name == "Michael"
    assert response.get_value("message")[0].surname == "Thompson"
    assert response.get_value("message")[0].birth == "1985-08-30"
    assert response.get_value("message")[0].nationality == "American"
    assert response.get_value("message")[0].created == "2025-02-20"
    assert response.get_value("message")[0].creator == "Michael Thompson"
    assert response.get_value("message")[0].last_editor == "Sarah Lee"
    assert response.get_value("message")[0].description == "A data scientist with expertise in machine learning and AI."
    assert response.get_value("message")[0].modified == "2025-02-22T14:45:00Z"

@pytest.mark.usefixtures("filmology_management_db_mock")
def test_get_director(client_mock, test_environment):
    request, response, _ = test_environment

    filmology_management_facade = initialize_facade(
        "filmology_app.components.FilmologyManagement.FilmologyManagement_facade.FilmologyManagement",
        request,
        response,
    )

    seed_database("filmology_management.db")

    request.set_value("client", client_mock)

    filmology_management_facade.execute("GETDirector")

    assert len(response.get_value("message")) == 1
    assert response.get_value("message")[0].name == "Michael"
    assert response.get_value("message")[0].surname == "Thompson"
    assert response.get_value("message")[0].birth == "1985-08-30"
    assert response.get_value("message")[0].nationality == "American"
    assert response.get_value("message")[0].created == "2025-02-20"
    assert response.get_value("message")[0].creator == "Michael Thompson"

@pytest.mark.usefixtures("filmology_management_db_mock")
def test_post_movie(client_mock, test_environment):
    request, response, _ = test_environment

    filmology_management_facade = initialize_facade(
        "filmology_app.components.FilmologyManagement.FilmologyManagement_facade.FilmologyManagement",
        request,
        response,
    )

    seed_database("filmology_management.db")

    request.set_value("client", client_mock)

    request.set_value("body", json.dumps({
        "created": "2025-02-20",
        "creator": "Jane Doe",
        "last_editor": "John Smith",
        "modified": "2025-02-21T15:30:00Z",
        "name": "Sample Project",
        "description": "This is a sample project demonstrating JSON schema usage.",
        "alias": "sample_project",
        "plot": "A brief overview of the project's objectives and scope.",
        "color": "#FF5733",
        "runtime": "120 minutes",
        "country": "Canada",
        "date": "2025-02-22",
        "URL": "https://www.example.com/sample_project",
        "CompositionPosterPrimary": "Poster:faa3b1b4-efdb-11ef-8b1b-60dd8ec76433",
        "Date": "Date:faa3b1b4-efdb-11ef-8b1b-60dd8ec76433",
    }).encode())

    filmology_management_facade.execute("POSTMovie")

    assert len(response.get_value("message")) == 1
    assert response.get_value("message")[0].name == "Sample Project"
    assert response.get_value("message")[0].alias == "sample_project"
    assert response.get_value("message")[0].plot == "A brief overview of the project's objectives and scope."
    assert response.get_value("message")[0].color == "#FF5733"
    assert response.get_value("message")[0].runtime == "120 minutes"
    assert response.get_value("message")[0].country == "Canada"
    assert response.get_value("message")[0].date == "2025-02-22"
    assert response.get_value("message")[0].URL == "https://www.example.com/sample_project"
    assert response.get_value("message")[0].created == "2025-02-20"
    assert response.get_value("message")[0].creator == "Jane Doe"
    assert response.get_value("message")[0].last_editor == "John Smith"
    assert response.get_value("message")[0].modified == "2025-02-21T15:30:00Z"

@pytest.mark.usefixtures("filmology_management_db_mock")
def test_get_movies(client_mock, test_environment):
    request, response, _ = test_environment

    filmology_management_facade = initialize_facade(
        "filmology_app.components.FilmologyManagement.FilmologyManagement_facade.FilmologyManagement",
        request,
        response,
    )

    seed_database("filmology_management.db")

    request.set_value("client", client_mock)

    filmology_management_facade.execute("GETMovie")

    assert len(response.get_value("message")) == 1
    assert response.get_value("message")[0].name == "Sample Project"
    assert response.get_value("message")[0].alias == "sample_project"
    assert response.get_value("message")[0].plot == "A brief overview of the project's objectives and scope."
    assert response.get_value("message")[0].color == "#FF5733"
    assert response.get_value("message")[0].runtime == "120 minutes"
    assert response.get_value("message")[0].country == "Canada"
    assert response.get_value("message")[0].date == "2025-02-22"
    assert response.get_value("message")[0].URL == "https://www.example.com/sample_project"
    assert response.get_value("message")[0].created == "2025-02-20"
    assert response.get_value("message")[0].creator == "Jane Doe"
    assert response.get_value("message")[0].last_editor == "John Smith"

@pytest.mark.usefixtures("filmology_management_db_mock")
def test_post_date(client_mock, test_environment):
    request, response, _ = test_environment

    filmology_management_facade = initialize_facade(
        "filmology_app.components.FilmologyManagement.FilmologyManagement_facade.FilmologyManagement",
        request,
        response,
    )

    seed_database("filmology_management.db")

    request.set_value("client", client_mock)

    request.set_value("body", json.dumps({
        "year": "2005",
        "name": "new day",
    }).encode())

    filmology_management_facade.execute("POSTDate")

    assert len(response.get_value("message")) == 1
    assert response.get_value("message")[0].year == "2005"
    assert response.get_value("message")[0].name == "new day"

@pytest.mark.usefixtures("filmology_management_db_mock")
def test_get_date(client_mock, test_environment):
    request, response, _ = test_environment

    filmology_management_facade = initialize_facade(
        "filmology_app.components.FilmologyManagement.FilmologyManagement_facade.FilmologyManagement",
        request,
        response,
    )

    seed_database("filmology_management.db")

    request.set_value("client", client_mock)

    filmology_management_facade.execute("GETDate")

    assert len(response.get_value("message")) == 2
    assert response.get_value("message")[1].year == "2005"
    assert response.get_value("message")[1].name == "new day"
