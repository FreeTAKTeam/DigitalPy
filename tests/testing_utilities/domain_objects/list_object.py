from typing import TYPE_CHECKING
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

if TYPE_CHECKING:
    from .simple_object import SimpleObject

class ListObject(Node):
    def __init__(self, model_configuration, model, oid=None, node_type="ListObject") -> None:
        super().__init__(model_configuration=model_configuration, model=model, node_type=node_type, oid=oid)
        self._string: str = None

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, string: str):
        self._string = string

    @Relationship(multiplicity_lower=0, multiplicity_upper=-1, reltype=RelationshipType.ASSOCIATION, navigable=True)
    def list_data(self) -> list['SimpleObject']:
        return self.get_children_ex(children_type="SimpleObject")
    
    @list_data.setter
    def list_data(self, list_data: list['SimpleObject']):
        self.add_child(list_data)