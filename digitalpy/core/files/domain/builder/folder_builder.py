from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId


from digitalpy.core.files.configuration.Files_constants import FOLDER

# import domain model classes
from digitalpy.core.files.domain.model.folder import Folder

from digitalpy.core.files.persistence.folder import Folder as DBFolder

class FolderBuilder(Builder):
    """Builds a Folder object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Folder = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a Folder object"""
        self.request.set_value("object_class_name", "Folder")

        configuration = config_loader.find_configuration(FOLDER)

        self.result = super()._create_model_object(
          configuration, extended_domain={"Folder": Folder,
                                        })

    def add_object_data(self, mapped_object: Union[bytes, str, DBFolder], protocol=None):
        """adds the data from the mapped object to the Health object """
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBFolder):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBFolder):
        """adds the data from the db object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.path = db_object.path
        self.result.size = db_object.size
        self.result.permissions = db_object.permissions
        self.result.name = db_object.name
    def get_result(self):
        """gets the result of the builder"""
        return self.result
