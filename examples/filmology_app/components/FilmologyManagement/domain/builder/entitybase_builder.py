from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId


from filmology_app.components.FilmologyManagement.configuration.FilmologyManagement_constants import ENTITYBASE

# import domain model classes
from filmology_app.components.FilmologyManagement.domain.model.entitybase import EntityBase

from filmology_app.components.FilmologyManagement.persistence.entitybase import EntityBase as DBEntityBase

class EntityBaseBuilder(Builder):
    """Builds a EntityBase object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: EntityBase = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a EntityBase object"""
        self.request.set_value("object_class_name", "EntityBase")

        configuration = config_loader.find_configuration(ENTITYBASE)

        self.result = super()._create_model_object(
          configuration, extended_domain={"EntityBase": EntityBase,
                                        })

    def add_object_data(self, mapped_object: Union[bytes, str, DBEntityBase], protocol=None):
        """adds the data from the mapped object to the Health object """
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBEntityBase):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBEntityBase):
        """adds the data from the db object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.creator = db_object.creator
        self.result.created = db_object.created
        self.result.last_editor = db_object.last_editor
        self.result.name = db_object.name
        self.result.modified = db_object.modified
    def get_result(self):
        """gets the result of the builder"""
        return self.result
