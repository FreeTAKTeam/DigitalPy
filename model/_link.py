from node import Node

class Link(Node):
    def __init__(self):
        super(Link, self).__init__(Link)

    def _instantiate_properties(self):
        self._properties["mime"] = None
        self._properties["parent_callsign"] = None
        self._properties["point"] = None
        self._properties["production_time"] = None
        self._properties["relation"] = None
        self._properties["type"] = None
        self._properties["uid"] = None
        self._properties["url"] = None
        self._properties["version"] = None