from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId


from digitalpy.core.component_management.configuration.component_management_constants import ACTIONKEY

# import domain model classes
from digitalpy.core.component_management.domain.model.actionkey import ActionKey
from digitalpy.core.component_management.domain.model.component import Component

from digitalpy.core.component_management.persistence.actionkey import ActionKey as DBActionKey

class ActionKeyBuilder(Builder):
    """Builds a ActionKey object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: ActionKey = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a ActionKey object"""
        self.request.set_value("object_class_name", "ActionKey")

        configuration = config_loader.find_configuration(ACTIONKEY)

        self.result = super()._create_model_object(
          configuration, extended_domain={"ActionKey": ActionKey,
                                            "Component": Component,
                                        })

    def add_object_data(self, mapped_object: Union[bytes, str, DBActionKey], protocol=None):
        """adds the data from the mapped object to the Health object """
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBActionKey):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBActionKey):
        """adds the data from the db object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.action = db_object.action
        self.result.context = db_object.context
        self.result.decorator = db_object.decorator
        self.result.config = db_object.config
        self.result.target = db_object.target
        self.result.source = db_object.source
        self.result.referencedBehaviour = db_object.referencedBehaviour
        self.result.name = db_object.name
    def get_result(self):
        """gets the result of the builder"""
        return self.result
