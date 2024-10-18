from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId


from digitalpy.core.telemetry.configuration.telemetry_constants import SERVICESTATUS

# import domain model classes
from digitalpy.core.service_management.domain.model.service_status import ServiceStatus

from digitalpy.core.service_management.persistence.service_status import (
    ServiceStatus as DBServiceStatus,
)


class ServiceStatusBuilder(Builder):
    """Builds a ServiceStatus object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: ServiceStatus = None  # type: ignore

    def build_empty_object(
        self, config_loader, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """Builds a ServiceStatus object"""
        self.request.set_value("object_class_name", "ServiceStatus")

        configuration = config_loader.find_configuration(SERVICESTATUS)

        self.result = super()._create_model_object(
            configuration,
            extended_domain={
                "ServiceStatus": ServiceStatus,
            },
        )

    def add_object_data(
        self, mapped_object: Union[bytes, str, DBServiceStatus], protocol=None
    ):
        """adds the data from the mapped object to the Health object"""
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBServiceStatus):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object"""
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBServiceStatus):
        """adds the data from the db object to the Health object"""
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.upTime = db_object.upTime
        self.result.lastError = db_object.lastError
        self.result.ServiceName = db_object.ServiceName
        self.result.ServiceStatus = db_object.ServiceStatus
        self.result.Port = db_object.Port
        self.result.name = db_object.name
        self.result.ServiceStatusActual = db_object.ServiceStatusActual

    def get_result(self):
        """gets the result of the builder"""
        return self.result
