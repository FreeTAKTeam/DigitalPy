from digitalpy.core.domain.node import Node

class SimpleList(Node):
    def __init__(self, model_configuration, model, oid=None, node_type="Contact") -> None:
        super().__init__(model_configuration=model_configuration, model=model, node_type=node_type, oid=oid)
        self._string: str = None
        self._number: int = None
        self._string_list: list = []

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, string: str):
        self._string = string

    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, number: str):
        self._number = number

    @property
    def string_list(self):
        return self._string_list
    
    @string_list.setter
    def string_list(self, string_list: list):
        self._string_list = string_list
