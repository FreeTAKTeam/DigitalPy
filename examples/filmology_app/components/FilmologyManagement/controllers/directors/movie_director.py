from typing import Union, Optional
from filmology_app.components.FilmologyManagement.domain.model.movie import Movie
from filmology_app.components.FilmologyManagement.persistence.movie import Movie as DBMovie
from filmology_app.components.FilmologyManagement.domain.builder.movie_builder import MovieBuilder
from filmology_app.components.FilmologyManagement.controllers.FilmologyManagement_persistence_controller import FilmologyManagementPersistenceController


from filmology_app.components.FilmologyManagement.domain.builder.poster_builder import PosterBuilder
from filmology_app.components.FilmologyManagement.domain.builder.date_builder import DateBuilder

from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.node import Node
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.parsing.load_configuration import LoadConfiguration


class MovieDirector(Controller):

    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.Movie_builder = MovieBuilder(request, response, sync_action_mapper, configuration)
        self.Poster_builder = PosterBuilder(request, response, sync_action_mapper, configuration)
        self.Date_builder = DateBuilder(request, response, sync_action_mapper, configuration)
        self.persistency_controller = FilmologyManagementPersistenceController(
            request, response, sync_action_mapper, configuration)


    def initialize(self, request, response):
        super().initialize(request, response)
        self.Movie_builder.initialize(request, response)
        self.Poster_builder.initialize(request, response)
        self.Date_builder.initialize(request, response)
        self.persistency_controller.initialize(request, response)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def construct_from_db(self, Movie: 'DBMovie', config_loader, base_object: 'Movie' = None, *args, **kwargs) -> 'Movie':
        """construct a node from a mapped object"""
        if (base_object):
            self.Movie_builder.result = base_object
        else:
            self.Movie_builder.build_empty_object(config_loader=config_loader)
        self.Movie_builder.add_object_data(mapped_object=Movie, protocol=None)
        Movie_completed = self.Movie_builder.get_result()

        CompositionPosterPrimary = Movie.CompositionPosterPrimary
        self.Poster_builder.build_empty_object(config_loader=config_loader)
        self.Poster_builder.add_object_data(mapped_object=CompositionPosterPrimary, protocol=None)
        Poster_completed = self.Poster_builder.get_result()
        Movie_completed.CompositionPosterPrimary = Poster_completed.oid
        Date = Movie.Date
        self.Date_builder.build_empty_object(config_loader=config_loader)
        self.Date_builder.add_object_data(mapped_object=Date, protocol=None)
        Date_completed = self.Date_builder.get_result()
        Movie_completed.Date = Date_completed.oid

        return Movie_completed

    def construct_from_json(self, Movie: Union[str, bytes], config_loader, base_object: Optional['Movie'] = None, *args, **kwargs) -> 'Movie':
        """construct a node from a mapped object"""
        # if the base_object is passed use it, otherwise build a new one
        if (base_object):
            self.Movie_builder.result = base_object
        else:
            self.Movie_builder.build_empty_object(config_loader=config_loader)

        # call the Movie builder to serialize the data into the object
        self.Movie_builder.add_object_data(mapped_object=Movie, protocol=Protocols.JSON)
        Movie_completed = self.Movie_builder.get_result()


        return Movie_completed
