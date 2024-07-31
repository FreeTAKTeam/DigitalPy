from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId


from digitalpy.core.files.configuration.Files_constants import ERROR

# import domain model classes
from digitalpy.core.files.domain.model.error import Error

from digitalpy.core.files.persistence.error import Error as DBError

class ErrorBuilder(Builder):
    """Builds a Error object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Error = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a Error object"""
        self.request.set_value("object_class_name", "Error")

        configuration = config_loader.find_configuration(ERROR)

        self.result = super()._create_model_object(
          configuration, extended_domain={"Error": Error,
                                        })

    def add_object_data(self, mapped_object: Union[bytes, str, DBError], protocol=None):
        """adds the data from the mapped object to the Health object """
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBError):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBError):
        """adds the data from the db object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.name = db_object.name
    def get_result(self):
        """gets the result of the builder"""
        return self.result
