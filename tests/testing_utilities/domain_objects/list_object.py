from digitalpy.core.domain.node import Node
from typing import TYPE_CHECKING

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

    @property
    def list_data(self) -> list['SimpleObject']:
        return self.get_children_ex(children_type="SimpleObject")
    
    @list_data.setter
    def list_data(self, list_data: list['SimpleObject']):
        self.add_child(list_data)