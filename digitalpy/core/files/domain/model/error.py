# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

from typing import TYPE_CHECKING
# iterating associations

class Error(Node):
    """Error"""
    def __init__(self, model_configuration, model, oid=None, node_type="Error") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._name: 'str' = None

    @property
    def name(self) -> 'str':
        """"""
        return self._name

    @name.setter
    def name(self, name: 'str'):
        name = str(name)
        if not isinstance(name, str):
            raise TypeError("'name' must be of type str")
        self._name= name
