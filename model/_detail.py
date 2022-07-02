from ctypes.wintypes import DWORD
from node import Node

class Detail(Node):
    def __init__(self):
        super(Detail, self).__init__(Detail)

    def _instantiate_properties(self):
        pass