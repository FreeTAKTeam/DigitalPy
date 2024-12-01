from typing import TYPE_CHECKING
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

if TYPE_CHECKING:
    from .simple_object import SimpleObject

class NestedObject(Node):
    def __init__(self, model_configuration, model, oid=None, node_type="NestedObject") -> None:
        super().__init__(model_configuration=model_configuration, model=model, node_type=node_type, oid=oid)
        self._string: str = None

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, string: str):
        self._string = string

    @Relationship(multiplicity_lower=0, multiplicity_upper=-1, reltype=RelationshipType.ASSOCIATION, navigable=True)
    def nested(self) -> 'SimpleObject':
        return_val = self.get_children_ex(children_type="SimpleObject")
        if len(return_val)>0:
            return return_val[0]
        else:
            return None
    
    @nested.setter
    def nested(self, nested: 'SimpleObject'):
        if self.nested is not None:
            self.delete_child(self.nested.oid)
        self.add_child(nested)
