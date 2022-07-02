from node import Node

class Emergency(Node):
    def __init__(self):
        super(Emergency, self).__init__(Emergency)
    
    def _instantiate_properties(self):
        self._properties["Alert"] = None
        self._properties["cancel"] = None
        self._properties["type"] = None