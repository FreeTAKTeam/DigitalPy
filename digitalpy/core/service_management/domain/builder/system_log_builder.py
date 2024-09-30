from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols


from digitalpy.core.telemetry.configuration.telemetry_constants import SYSTEMLOG

# import domain model classes
from digitalpy.core.service_management.domain.model.system_log import SystemLog

from digitalpy.core.service_management.persistence.system_log import SystemLog as DBSystemLog

class SystemLogBuilder(Builder):
    """Builds a SystemLog object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: SystemLog = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a SystemLog object"""
        self.request.set_value("object_class_name", "SystemLog")

        configuration = config_loader.find_configuration(SYSTEMLOG)

        self.result = super()._create_model_object(
          configuration, extended_domain={"SystemLog": SystemLog,
                                        })

    def add_object_data(self, mapped_object: Union[bytes, str, DBSystemLog], protocol=None):
        """adds the data from the mapped object to the Health object """
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBSystemLog):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBSystemLog):
        """adds the data from the db object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.severity = db_object.severity
        self.result.file = db_object.file
        self.result.name = db_object.name
        self.result.message = db_object.message
        self.result.Name = db_object.Name
        self.result.timestamp = db_object.timestamp
    def get_result(self):
        """gets the result of the builder"""
        return self.result
