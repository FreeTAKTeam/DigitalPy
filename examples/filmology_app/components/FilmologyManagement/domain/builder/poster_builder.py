from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId


from filmology_app.components.FilmologyManagement.configuration.FilmologyManagement_constants import POSTER

# import domain model classes
from filmology_app.components.FilmologyManagement.domain.model.poster import Poster
from filmology_app.components.FilmologyManagement.domain.model.movie import Movie
from filmology_app.components.FilmologyManagement.domain.model.actor import Actor
from filmology_app.components.FilmologyManagement.domain.model.date import Date
from filmology_app.components.FilmologyManagement.domain.model.director import Director

from filmology_app.components.FilmologyManagement.persistence.poster import Poster as DBPoster
from filmology_app.components.FilmologyManagement.persistence.movie import Movie as DBMovie
from filmology_app.components.FilmologyManagement.persistence.actor import Actor as DBActor
from filmology_app.components.FilmologyManagement.persistence.date import Date as DBDate
from filmology_app.components.FilmologyManagement.persistence.director import Director as DBDirector

class PosterBuilder(Builder):
    """Builds a Poster object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Poster = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a Poster object"""
        self.request.set_value("object_class_name", "Poster")

        configuration = config_loader.find_configuration(POSTER)

        self.result = super()._create_model_object(
          configuration, extended_domain={"Poster": Poster,
                                            "Movie": Movie,
                                            "Actor": Actor,
                                            "Date": Date,
                                            "Director": Director,
                                        })

    def add_object_data(self, mapped_object: Union[bytes, str, DBPoster], protocol=None):
        """adds the data from the mapped object to the Health object """
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBPoster):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBPoster):
        """adds the data from the db object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.name = db_object.name
    def get_result(self):
        """gets the result of the builder"""
        return self.result
