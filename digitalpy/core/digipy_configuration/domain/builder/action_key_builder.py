from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.digipy_configuration.domain.model.actionkey import ActionKey

from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    ACTION_KEY,
)
from digitalpy.core.zmanager.domain.model.topic import Topic


class ActionKeyBuilder(Builder):
    """Builds an action key object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Topic = None  # type: ignore

    def build_empty_object(
        self, config_loader=None, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """Builds an action_key object, config_loader is None because it is not used"""
        self.request.set_value("object_class_name", "ActionKey")

        configuration = config_loader.find_configuration(ACTION_KEY)

        self.result = super()._create_model_object(
            configuration,
            extended_domain={
                "ActionKey": ActionKey,
            },
        )

    def add_object_data(self, mapped_object: Union[bytes, str], protocol=None):
        """adds the data from the mapped object to the action key object"""
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the action key object"""
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def get_result(self):
        """gets the result of the builder"""
        return self.result
