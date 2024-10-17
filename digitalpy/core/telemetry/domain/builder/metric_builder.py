from typing import Union
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId


from digitalpy.core.telemetry.configuration.telemetry_constants import METRIC

# import domain model classes
from digitalpy.core.telemetry.domain.model.metric import Metric

from digitalpy.core.telemetry.persistence.metric import Metric as DBMetric

class MetricBuilder(Builder):
    """Builds a Metric object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Metric = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a Metric object"""
        self.request.set_value("object_class_name", "Metric")

        configuration = config_loader.find_configuration(METRIC)

        self.result = super()._create_model_object(
          configuration, extended_domain={"Metric": Metric,
                                        })

    def add_object_data(self, mapped_object: Union[bytes, str, DBMetric], protocol=None):
        """adds the data from the mapped object to the Health object """
        if protocol == Protocols.JSON and isinstance(mapped_object, bytes):
            self._add_json_object_data(mapped_object)

        elif isinstance(mapped_object, DBMetric):
            self._add_db_object_data(mapped_object)

    def _add_json_object_data(self, json_object: bytes):
        """adds the data from the json object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", json_object)
        self.request.set_value("protocol", Protocols.JSON)
        self.execute_sub_action("deserialize")

    def _add_db_object_data(self, db_object: DBMetric):
        """adds the data from the db object to the Health object """
        self.request.set_value("model_object", self.result)
        self.request.set_value("message", db_object)
        self.result.oid = db_object.oid
        self.result.unit = db_object.unit
        self.result.metricName = db_object.metricName
        self.result.valueExpected = db_object.valueExpected
        self.result.name = db_object.name
        self.result.description = db_object.description
        self.result.ID = db_object.ID
        self.result.value = db_object.value
        self.result.timestamp = db_object.timestamp
    def get_result(self):
        """gets the result of the builder"""
        return self.result
