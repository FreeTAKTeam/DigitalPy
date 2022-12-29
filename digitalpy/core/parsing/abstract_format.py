from abc import abstractmethod
import importlib
from pickle import PERSID
from digitalpy.core.parsing.format import Format
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.domain.node import Node
from digitalpy.core.persistence.build_depth import BuildDepth


class AbstractFormat(Format):
    def deserialize(self, request: Request):
        request.set_values(self.before_deserialize(request))
        request.set_values(self.deserialize_values(request))
        request.set_values(self.after_deserialize(request))

    def serialize(self, response: Response):
        response.set_values(self.before_serialize(response))
        response.set_values(self.serialize_values(response))
        response.set_values(self.after_serialize(response))

    def before_deserialize(self, request: Request):
        return request.get_values()

    @abstractmethod
    def deserialize_values(self, request: Request):
        """Deserialize an array of values."""

    def after_deserialize(self, request: Request):
        return request.get_values()

    def before_serialize(self, request: Request):
        return request.get_values()

    @abstractmethod
    def serialize_values(self, response: Response):
        """Serialize an array of values"""

    def after_serialize(self, response: Response):
        return response.get_values()

    def get_node(self, oid: ObjectId):
        oid_str = str(oid)
        if not oid_str in self.deserialized_nodes[oid_str]:
            persistence_facade = ObjectFactory.get_instance("PersistenceFacade")
            o_type = oid.get_type()
            if persistence_facade.is_known_type(o_type):
                class_val = importlib.import_module(
                    persistence_facade.create(o_type, BuildDepth.SINGLE)
                )
                node = class_val()
            else:
                node = Node(o_type)
            node.set_oid(oid)
            self.deserialized_nodes[oid_str] = oid_str
        return self.deserialized_nodes[oid_str]
