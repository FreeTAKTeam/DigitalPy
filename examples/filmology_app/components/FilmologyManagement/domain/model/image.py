# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

from typing import TYPE_CHECKING
# iterating associations

class Image(Node):
    """"""
    def __init__(self, model_configuration, model, oid=None, node_type="Image") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._fileName: 'str' = None
        self._name: 'str' = None

    @property
    def fileName(self) -> 'str':
        """"""
        return self._fileName

    @fileName.setter
    def fileName(self, fileName: 'str'):
        fileName = str(fileName)
        if not isinstance(fileName, str):
            raise TypeError("'fileName' must be of type str")
        self._fileName= fileName

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
