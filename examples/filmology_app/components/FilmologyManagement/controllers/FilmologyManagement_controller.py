"""
This is the main controller class of the application. Every operation of the controller is realized by this file
OOTB. It is recommended that you (the developper) avoid adding further methods to the file and instead add supporting
controllers with these methods should you need them. This controller is called directly by the facade in order to
fulfil any requests made to the component by default.
"""

from typing import TYPE_CHECKING, List

from digitalpy.core.main.controller import Controller
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
# import builders
from filmology_app.components.FilmologyManagement.domain.builder.actor_builder import ActorBuilder
from filmology_app.components.FilmologyManagement.domain.builder.person_builder import PersonBuilder
from filmology_app.components.FilmologyManagement.domain.builder.entitybaseextended_builder import EntityBaseExtendedBuilder
from filmology_app.components.FilmologyManagement.domain.builder.entitybase_builder import EntityBaseBuilder
from filmology_app.components.FilmologyManagement.controllers.directors.date_director import DateDirector
from filmology_app.components.FilmologyManagement.domain.builder.date_builder import DateBuilder
from filmology_app.components.FilmologyManagement.controllers.directors.movie_director import MovieDirector
from filmology_app.components.FilmologyManagement.domain.builder.movie_builder import MovieBuilder
from filmology_app.components.FilmologyManagement.domain.builder.poster_builder import PosterBuilder
from filmology_app.components.FilmologyManagement.domain.builder.image_builder import ImageBuilder
from filmology_app.components.FilmologyManagement.domain.builder.director_builder import DirectorBuilder
from filmology_app.components.FilmologyManagement.domain.builder.genre_builder import GenreBuilder
from filmology_app.components.FilmologyManagement.domain.builder.language_builder import LanguageBuilder
from filmology_app.components.FilmologyManagement.domain.builder.error_builder import ErrorBuilder
from .FilmologyManagement_persistence_controller import FilmologyManagementPersistenceController

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient
    from filmology_app.components.FilmologyManagement.domain.model.actor import Actor
    from filmology_app.components.FilmologyManagement.domain.model.person import Person
    from filmology_app.components.FilmologyManagement.domain.model.entitybaseextended import EntityBaseExtended
    from filmology_app.components.FilmologyManagement.domain.model.entitybase import EntityBase
    from filmology_app.components.FilmologyManagement.domain.model.date import Date
    from filmology_app.components.FilmologyManagement.domain.model.movie import Movie
    from filmology_app.components.FilmologyManagement.domain.model.poster import Poster
    from filmology_app.components.FilmologyManagement.domain.model.image import Image
    from filmology_app.components.FilmologyManagement.domain.model.director import Director
    from filmology_app.components.FilmologyManagement.domain.model.genre import Genre
    from filmology_app.components.FilmologyManagement.domain.model.language import Language
    from filmology_app.components.FilmologyManagement.domain.model.error import Error

class FilmologyManagementController(Controller):

    def __init__(self, request: 'Request',
                 response: 'Response',
                 sync_action_mapper: 'DefaultActionMapper',
                 configuration: 'Configuration'):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.Actor_builder = ActorBuilder(request, response, sync_action_mapper, configuration)
        self.Person_builder = PersonBuilder(request, response, sync_action_mapper, configuration)
        self.Entitybaseextended_builder = EntityBaseExtendedBuilder(request, response, sync_action_mapper, configuration)
        self.Entitybase_builder = EntityBaseBuilder(request, response, sync_action_mapper, configuration)
        self.Date_director = DateDirector(request, response, sync_action_mapper, configuration)
        self.Date_builder = DateBuilder(request, response, sync_action_mapper, configuration)
        self.Movie_director = MovieDirector(request, response, sync_action_mapper, configuration)
        self.Movie_builder = MovieBuilder(request, response, sync_action_mapper, configuration)
        self.Poster_builder = PosterBuilder(request, response, sync_action_mapper, configuration)
        self.Image_builder = ImageBuilder(request, response, sync_action_mapper, configuration)
        self.Director_builder = DirectorBuilder(request, response, sync_action_mapper, configuration)
        self.Genre_builder = GenreBuilder(request, response, sync_action_mapper, configuration)
        self.Language_builder = LanguageBuilder(request, response, sync_action_mapper, configuration)
        self.Error_builder = ErrorBuilder(request, response, sync_action_mapper, configuration)
        self.persistence_controller = FilmologyManagementPersistenceController(
            request, response, sync_action_mapper, configuration)

    def initialize(self, request: 'Request', response: 'Response'):
        """This function is used to initialize the controller. 
        It is intiated by the service manager."""
        self.Actor_builder.initialize(request, response)
        self.Person_builder.initialize(request, response)
        self.Entitybaseextended_builder.initialize(request, response)
        self.Entitybase_builder.initialize(request, response)
        self.Date_director.initialize(request, response)
        self.Date_builder.initialize(request, response)
        self.Movie_director.initialize(request, response)
        self.Movie_builder.initialize(request, response)
        self.Poster_builder.initialize(request, response)
        self.Image_builder.initialize(request, response)
        self.Director_builder.initialize(request, response)
        self.Genre_builder.initialize(request, response)
        self.Language_builder.initialize(request, response)
        self.Error_builder.initialize(request, response)
        self.persistence_controller.initialize(request, response)
        return super().initialize(request, response)
    def POSTMovie(self, body: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # initialize Movie builder
        domain_obj  = self.Movie_director.construct_from_json(body, config_loader)

        # Save the Movie record to the database
        self.persistence_controller.save_movie(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def DELETEMovie(self, ID: str, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        db_records = self.persistence_controller.get_movie(ID = ID)
        domain_records: List['Movie'] = []

        # convert the records to the domain object
        for record in db_records:
            record = self.Movie_director.construct_from_db(record, config_loader)
            self.persistence_controller.remove_movie(record)
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def GETMovie(self, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # retrieve the Movie record from the database
        db_records = self.persistence_controller.get_all_movie()
        domain_records: List['Movie'] = []

        # convert the records to the domain object
        for record in db_records:
            Movie = self.Movie_director.construct_from_db(record, config_loader)
            domain_records.append(Movie)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def PATCHMovie(self, body: 'Movie',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # create the basic domain object from the json data
        self.Movie_builder.build_empty_object(config_loader)
        self.Movie_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Movie_builder.get_result()

        # get from the database
        db_obj = self.persistence_controller.get_movie(oid=str(domain_obj.oid))[0]

        # initialize the object
        self.Movie_director.construct_from_db(db_obj, config_loader, domain_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        domain_obj = self.Movie_director.construct_from_json(body, config_loader, domain_obj)
        # Save the Schedule record to the database
        self.persistence_controller.update_movie(domain_obj)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

    def GETDirectorId(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # retrieve the Director record from the database
        db_records = self.persistence_controller.get_director(ID = ID)
        domain_records: List['Director'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Director_builder.build_empty_object(config_loader=config_loader)
            self.Director_builder.add_object_data(record)
            domain_records.append(self.Director_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def POSTPoster(self, body: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # initialize Poster builder
        self.Poster_builder.build_empty_object(config_loader=config_loader)
        self.Poster_builder.add_object_data(mapped_object = body, protocol=Protocols.JSON)
        domain_obj = self.Poster_builder.get_result()

        # Save the Poster record to the database
        self.persistence_controller.save_poster(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def DELETEPoster(self, ID: str, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        db_records = self.persistence_controller.get_poster(ID = ID)
        domain_records: List['Poster'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Poster_builder.build_empty_object(config_loader=config_loader)
            self.Poster_builder.add_object_data(record)
            record = self.Poster_builder.get_result()
            self.persistence_controller.remove_poster(record)
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def GETPoster(self, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # retrieve the Poster record from the database
        db_records = self.persistence_controller.get_all_poster()
        domain_records: List['Poster'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Poster_builder.build_empty_object(config_loader=config_loader)
            self.Poster_builder.add_object_data(record)
            domain_records.append(self.Poster_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def PATCHPoster(self, body: 'Poster',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # create the basic domain object from the json data
        self.Poster_builder.build_empty_object(config_loader)
        self.Poster_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Poster_builder.get_result()

        # get from the database
        db_obj = self.persistence_controller.get_poster(oid=str(domain_obj.oid))[0]

        # initialize the object
        self.Poster_builder.build_empty_object(config_loader)
        self.Poster_builder.add_object_data(db_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        self.Poster_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Poster_builder.get_result()
        # Save the Schedule record to the database
        self.persistence_controller.update_poster(domain_obj)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

    def GETGenreId(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # retrieve the Genre record from the database
        db_records = self.persistence_controller.get_genre(ID = ID)
        domain_records: List['Genre'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Genre_builder.build_empty_object(config_loader=config_loader)
            self.Genre_builder.add_object_data(record)
            domain_records.append(self.Genre_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def POSTDate(self, body: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # initialize Date builder
        domain_obj  = self.Date_director.construct_from_json(body, config_loader)

        # Save the Date record to the database
        self.persistence_controller.save_date(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def DELETEDate(self, ID: str, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        db_records = self.persistence_controller.get_date(ID = ID)
        domain_records: List['Date'] = []

        # convert the records to the domain object
        for record in db_records:
            record = self.Date_director.construct_from_db(record, config_loader)
            self.persistence_controller.remove_date(record)
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def GETDate(self, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # retrieve the Date record from the database
        db_records = self.persistence_controller.get_all_date()
        domain_records: List['Date'] = []

        # convert the records to the domain object
        for record in db_records:
            Date = self.Date_director.construct_from_db(record, config_loader)
            domain_records.append(Date)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def PATCHDate(self, body: 'Date',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # create the basic domain object from the json data
        self.Date_builder.build_empty_object(config_loader)
        self.Date_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Date_builder.get_result()

        # get from the database
        db_obj = self.persistence_controller.get_date(oid=str(domain_obj.oid))[0]

        # initialize the object
        self.Date_director.construct_from_db(db_obj, config_loader, domain_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        domain_obj = self.Date_director.construct_from_json(body, config_loader, domain_obj)
        # Save the Schedule record to the database
        self.persistence_controller.update_date(domain_obj)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

    def GETLanguageId(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # retrieve the Language record from the database
        db_records = self.persistence_controller.get_language(ID = ID)
        domain_records: List['Language'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Language_builder.build_empty_object(config_loader=config_loader)
            self.Language_builder.add_object_data(record)
            domain_records.append(self.Language_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def POSTDirector(self, body: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # initialize Director builder
        self.Director_builder.build_empty_object(config_loader=config_loader)
        self.Director_builder.add_object_data(mapped_object = body, protocol=Protocols.JSON)
        domain_obj = self.Director_builder.get_result()

        # Save the Director record to the database
        self.persistence_controller.save_director(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def DELETEDirector(self, ID: str, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        db_records = self.persistence_controller.get_director(ID = ID)
        domain_records: List['Director'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Director_builder.build_empty_object(config_loader=config_loader)
            self.Director_builder.add_object_data(record)
            record = self.Director_builder.get_result()
            self.persistence_controller.remove_director(record)
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def GETDirector(self, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # retrieve the Director record from the database
        db_records = self.persistence_controller.get_all_director()
        domain_records: List['Director'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Director_builder.build_empty_object(config_loader=config_loader)
            self.Director_builder.add_object_data(record)
            domain_records.append(self.Director_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def PATCHDirector(self, body: 'Director',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # create the basic domain object from the json data
        self.Director_builder.build_empty_object(config_loader)
        self.Director_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Director_builder.get_result()

        # get from the database
        db_obj = self.persistence_controller.get_director(oid=str(domain_obj.oid))[0]

        # initialize the object
        self.Director_builder.build_empty_object(config_loader)
        self.Director_builder.add_object_data(db_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        self.Director_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Director_builder.get_result()
        # Save the Schedule record to the database
        self.persistence_controller.update_director(domain_obj)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

    def GETDateId(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # retrieve the Date record from the database
        db_records = self.persistence_controller.get_date(ID = ID)
        domain_records: List['Date'] = []

        # convert the records to the domain object
        for record in db_records:
            Date = self.Date_director.construct_from_db(record, config_loader)
            domain_records.append(Date)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def POSTActor(self, body: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # initialize Actor builder
        self.Actor_builder.build_empty_object(config_loader=config_loader)
        self.Actor_builder.add_object_data(mapped_object = body, protocol=Protocols.JSON)
        domain_obj = self.Actor_builder.get_result()

        # Save the Actor record to the database
        self.persistence_controller.save_actor(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def DELETEActor(self, ID: str, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        db_records = self.persistence_controller.get_actor(ID = ID)
        domain_records: List['Actor'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Actor_builder.build_empty_object(config_loader=config_loader)
            self.Actor_builder.add_object_data(record)
            record = self.Actor_builder.get_result()
            self.persistence_controller.remove_actor(record)
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def GETActor(self, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # retrieve the Actor record from the database
        db_records = self.persistence_controller.get_all_actor()
        domain_records: List['Actor'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Actor_builder.build_empty_object(config_loader=config_loader)
            self.Actor_builder.add_object_data(record)
            domain_records.append(self.Actor_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def PATCHActor(self, body: 'Actor',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # create the basic domain object from the json data
        self.Actor_builder.build_empty_object(config_loader)
        self.Actor_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Actor_builder.get_result()

        # get from the database
        db_obj = self.persistence_controller.get_actor(oid=str(domain_obj.oid))[0]

        # initialize the object
        self.Actor_builder.build_empty_object(config_loader)
        self.Actor_builder.add_object_data(db_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        self.Actor_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Actor_builder.get_result()
        # Save the Schedule record to the database
        self.persistence_controller.update_actor(domain_obj)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

    def GETMovieId(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # retrieve the Movie record from the database
        db_records = self.persistence_controller.get_movie(ID = ID)
        domain_records: List['Movie'] = []

        # convert the records to the domain object
        for record in db_records:
            Movie = self.Movie_director.construct_from_db(record, config_loader)
            domain_records.append(Movie)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def POSTLanguage(self, body: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # initialize Language builder
        self.Language_builder.build_empty_object(config_loader=config_loader)
        self.Language_builder.add_object_data(mapped_object = body, protocol=Protocols.JSON)
        domain_obj = self.Language_builder.get_result()

        # Save the Language record to the database
        self.persistence_controller.save_language(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def DELETELanguage(self, ID: str, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        db_records = self.persistence_controller.get_language(ID = ID)
        domain_records: List['Language'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Language_builder.build_empty_object(config_loader=config_loader)
            self.Language_builder.add_object_data(record)
            record = self.Language_builder.get_result()
            self.persistence_controller.remove_language(record)
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def GETLanguage(self, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # retrieve the Language record from the database
        db_records = self.persistence_controller.get_all_language()
        domain_records: List['Language'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Language_builder.build_empty_object(config_loader=config_loader)
            self.Language_builder.add_object_data(record)
            domain_records.append(self.Language_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def PATCHLanguage(self, body: 'Language',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # create the basic domain object from the json data
        self.Language_builder.build_empty_object(config_loader)
        self.Language_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Language_builder.get_result()

        # get from the database
        db_obj = self.persistence_controller.get_language(oid=str(domain_obj.oid))[0]

        # initialize the object
        self.Language_builder.build_empty_object(config_loader)
        self.Language_builder.add_object_data(db_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        self.Language_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Language_builder.get_result()
        # Save the Schedule record to the database
        self.persistence_controller.update_language(domain_obj)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

    def GETPosterId(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # retrieve the Poster record from the database
        db_records = self.persistence_controller.get_poster(ID = ID)
        domain_records: List['Poster'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Poster_builder.build_empty_object(config_loader=config_loader)
            self.Poster_builder.add_object_data(record)
            domain_records.append(self.Poster_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def GETActorId(self, ID: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # retrieve the Actor record from the database
        db_records = self.persistence_controller.get_actor(ID = ID)
        domain_records: List['Actor'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Actor_builder.build_empty_object(config_loader=config_loader)
            self.Actor_builder.add_object_data(record)
            domain_records.append(self.Actor_builder.get_result())

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def POSTGenre(self, body: 'str', client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""

        # initialize Genre builder
        self.Genre_builder.build_empty_object(config_loader=config_loader)
        self.Genre_builder.add_object_data(mapped_object = body, protocol=Protocols.JSON)
        domain_obj = self.Genre_builder.get_result()

        # Save the Genre record to the database
        self.persistence_controller.save_genre(domain_obj)

        domain_records = [domain_obj]
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def DELETEGenre(self, ID: str, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        db_records = self.persistence_controller.get_genre(ID = ID)
        domain_records: List['Genre'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Genre_builder.build_empty_object(config_loader=config_loader)
            self.Genre_builder.add_object_data(record)
            record = self.Genre_builder.get_result()
            self.persistence_controller.remove_genre(record)
            domain_records.append(record)
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def GETGenre(self, client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # retrieve the Genre record from the database
        db_records = self.persistence_controller.get_all_genre()
        domain_records: List['Genre'] = []

        # convert the records to the domain object
        for record in db_records:
            self.Genre_builder.build_empty_object(config_loader=config_loader)
            self.Genre_builder.add_object_data(record)
            domain_records.append(self.Genre_builder.get_result())
        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", domain_records)

    def PATCHGenre(self, body: 'Genre',  client: 'NetworkClient', config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """"""
        # create the basic domain object from the json data
        self.Genre_builder.build_empty_object(config_loader)
        self.Genre_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Genre_builder.get_result()

        # get from the database
        db_obj = self.persistence_controller.get_genre(oid=str(domain_obj.oid))[0]

        # initialize the object
        self.Genre_builder.build_empty_object(config_loader)
        self.Genre_builder.add_object_data(db_obj)
        # TODO: this duplaction seems unnecessary
        # update the object with json data
        self.Genre_builder.add_object_data(body, Protocols.JSON)
        domain_obj = self.Genre_builder.get_result()
        # Save the Schedule record to the database
        self.persistence_controller.update_genre(domain_obj)

        # set the target
        self.response.set_value("recipients", [str(client.get_oid())])

        # return the records
        self.response.set_value("message", [domain_obj])

