from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId


from digitalpy.core.component_management.configuration.component_management_constants import COMPONENT

# import domain model classes
from digitalpy.core.component_management.domain.model.component import Component
from digitalpy.core.component_management.domain.model.actionkey import ActionKey

from digitalpy.core.component_management.persistence.component import Component as DBComponent
from digitalpy.core.component_management.persistence.actionkey import ActionKey as DBActionKey

class ComponentBuilder(Builder):
    """Builds a Component object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Component = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a Component object"""
        self.request.set_value("object_class_name", "Component")

        configuration = config_loader.find_configuration(COMPONENT)

        self.result = super()._create_model_object(
          configuration, extended_domain={"Component": Component,
                                            "ActionKey": ActionKey,
                                        })

    def add_object_data(self, mapped_object: Union[bytes, str, DBComponent], protocol=None):
        """adds the data from the mapped object to the Health object """
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBComponent):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBComponent):
        """adds the data from the db object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.author = db_object.author
        self.result.author_email = db_object.author_email
        self.result.description = db_object.description
        self.result.License = db_object.License
        self.result.repo = db_object.repo
        self.result.requiredAlfaVersion = db_object.requiredAlfaVersion
        self.result.URL = db_object.URL
        self.result.Version = db_object.Version
        self.result.UUID = db_object.UUID
        self.result.isActive = db_object.isActive
        self.result.isInstalled = db_object.isInstalled
        self.result.installationPath = db_object.installationPath
        self.result.name = db_object.name
    def get_result(self):
        """gets the result of the builder"""
        return self.result
