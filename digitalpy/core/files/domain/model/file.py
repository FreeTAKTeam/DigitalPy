# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

from typing import TYPE_CHECKING
# iterating associations

class File(Node):
    """"""
    def __init__(self, model_configuration, model, oid=None, node_type="File") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._path: 'str' = None
        self._permissions: 'str' = None
        self._size: 'float' = None
        self._name: 'str' = None

    @property
    def path(self) -> 'str':
        """"""
        return self._path

    @path.setter
    def path(self, path: 'str'):
        path = str(path)
        if not isinstance(path, str):
            raise TypeError("'path' must be of type str")
        self._path= path

    @property
    def permissions(self) -> 'str':
        """"""
        return self._permissions

    @permissions.setter
    def permissions(self, permissions: 'str'):
        permissions = str(permissions)
        if not isinstance(permissions, str):
            raise TypeError("'permissions' must be of type str")
        self._permissions= permissions

    @property
    def size(self) -> 'float':
        """"""
        return self._size

    @size.setter
    def size(self, size: 'float'):
        size = float(size)
        if not isinstance(size, float):
            raise TypeError("'size' must be of type float")
        self._size= size

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

    def __eq__(self, other: 'File') -> bool:
        if isinstance(other, File):
            return self.path == other.path or self.oid == other.oid
        return False