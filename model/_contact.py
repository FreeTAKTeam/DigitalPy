from node import Node

class Contact(Node):
    def __init__(self):
        super(Contact, self).__init__(Contact)

    def _instantiate_properties(self):
        self._properties["callsign"] = None
        self._properties["dsn"] = None
        self._properties["email"] = None
        self._properties["endpoint"] = None
        self._properties["freq"] = None
        self._properties["hostname"] = None
        self._properties["iconsetpath"] = None
        self._properties["modulation"] = None
        self._properties["phone"] = None
        self._properties["version"] = None