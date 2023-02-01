from digitalpy.core.domain.node import Node

class Connection(Node):
    def __init__(self, node_type = "connection", oid=None) -> None:
        super().__init__(node_type, oid=oid)
        self._service_id = None
        self._protocol = None

    @property
    def service_id(self):
        return self._service_id

    @service_id.setter
    def service_id(self, service_id: str):
        self._service_id = service_id

    @property
    def protocol(self):
        return self._protocol
    
    @protocol.setter
    def protocol(self, protocol: str):
        self._protocol = protocol