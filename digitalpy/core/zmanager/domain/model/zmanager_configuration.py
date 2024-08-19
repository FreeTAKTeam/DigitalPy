from digitalpy.core.domain.node import Node


class ZManagerConfiguration(Node):
    """ZManagerConfiguration class to represent the ZManager configuration."""
    def __init__(
        self, model_configuration, model, oid=None, node_type="ZManagerConfiguration"
    ) -> None:
        super().__init__(
            node_type, model_configuration=model_configuration, model=model, oid=oid
        )
        self._integration_manager_pub_address: str = None
        self._integration_manager_pub_sndhwm: int = None
        
        self._integration_manager_pull_address: str = None
        self._integration_manager_pull_timeout: int = None
        self._integration_manager_pull_rcvhwm: int = None

        self._subject_pull_address: str = None
        self._subject_pull_timeout: int = None

        self._subject_push_address: str = None
        self._subject_push_heartbeat_ivl: int = None
        self._subject_push_heartbeat_timeout: int = None
        self._subject_push_heartbeat_ttl: int = None
        self._subject_push_timeout: int = None
        
        self._worker_count: int = None
        self._worker_timeout: int = None


    @property
    def integration_manager_pub_address(self) -> "str":
        """The integration manager publish address."""
        return self._integration_manager_pub_address

    @integration_manager_pub_address.setter
    def integration_manager_pub_address(self, integration_manager_pub_address: "str"):
        integration_manager_pub_address = str(integration_manager_pub_address)
        if not isinstance(integration_manager_pub_address, str):
            raise TypeError("'integration_manager_pub_address' must be of type str")
        self._integration_manager_pub_address = integration_manager_pub_address

    @property
    def integration_manager_pull_address(self) -> "str":
        """The integration manager pull address."""
        return self._integration_manager_pull_address

    @integration_manager_pull_address.setter
    def integration_manager_pull_address(self, integration_manager_pull_address: "str"):
        integration_manager_pull_address = str(integration_manager_pull_address)
        if not isinstance(integration_manager_pull_address, str):
            raise TypeError("'integration_manager_pull_address' must be of type str")
        self._integration_manager_pull_address = integration_manager_pull_address

    @property
    def subject_pull_address(self) -> "str":
        """The subject pull address."""
        return self._subject_pull_address

    @subject_pull_address.setter
    def subject_pull_address(self, subject_pull_address: "str"):
        subject_pull_address = str(subject_pull_address)
        if not isinstance(subject_pull_address, str):
            raise TypeError("'subject_pull_address' must be of type str")
        self._subject_pull_address = subject_pull_address

    @property
    def subject_push_address(self) -> "str":
        """The subject push address."""
        return self._subject_push_address

    @subject_push_address.setter
    def subject_push_address(self, subject_push_address: "str"):
        subject_push_address = str(subject_push_address)
        if not isinstance(subject_push_address, str):
            raise TypeError("'subject_push_address' must be of type str")
        self._subject_push_address = subject_push_address

    @property
    def worker_count(self) -> "int":
        """The worker count."""
        return self._worker_count
    
    @worker_count.setter
    def worker_count(self, worker_count: "int"):
        worker_count = int(worker_count)
        if not isinstance(worker_count, int):
            raise TypeError("'worker_count' must be of type int")
        self._worker_count = worker_count

    @property
    def subject_pull_timeout(self) -> "int":
        """The subject socket timeout."""
        return self._subject_pull_timeout
    
    @subject_pull_timeout.setter
    def subject_pull_timeout(self, subject_pull_timeout: "int"):
        subject_pull_timeout = int(subject_pull_timeout)
        if not isinstance(subject_pull_timeout, int):
            raise TypeError("'subject_socket_timeout' must be of type int")
        self._subject_pull_timeout = subject_pull_timeout

    @property
    def integration_manager_pull_timeout(self) -> "int":
        """The integration manager socket timeout."""
        return self._integration_manager_pull_timeout

    @integration_manager_pull_timeout.setter
    def integration_manager_pull_timeout(self, integration_manager_pull_timeout: "int"):
        integration_manager_pull_timeout = int(integration_manager_pull_timeout)
        if not isinstance(integration_manager_pull_timeout, int):
            raise TypeError("'integration_manager_socket_timeout' must be of type int")
        self._integration_manager_pull_timeout = integration_manager_pull_timeout
    
    @property
    def subject_push_heartbeat_ivl(self) -> "int":
        """The subject push heartbeat interval."""
        return self._subject_push_heartbeat_ivl
    
    @subject_push_heartbeat_ivl.setter
    def subject_push_heartbeat_ivl(self, subject_push_heartbeat_ivl: "int"):
        subject_push_heartbeat_ivl = int(subject_push_heartbeat_ivl)
        if not isinstance(subject_push_heartbeat_ivl, int):
            raise TypeError("'subject_push_heartbeat_ivl' must be of type int")
        self._subject_push_heartbeat_ivl = subject_push_heartbeat_ivl

    @property
    def subject_push_heartbeat_timeout(self) -> "int":
        """The subject push heartbeat timeout."""
        return self._subject_push_heartbeat_timeout
    
    @subject_push_heartbeat_timeout.setter
    def subject_push_heartbeat_timeout(self, subject_push_heartbeat_timeout: "int"):
        subject_push_heartbeat_timeout = int(subject_push_heartbeat_timeout)
        if not isinstance(subject_push_heartbeat_timeout, int):
            raise TypeError("'subject_push_heartbeat_timeout' must be of type int")
        self._subject_push_heartbeat_timeout = subject_push_heartbeat_timeout

    @property
    def subject_push_heartbeat_ttl(self) -> "int":
        """The subject push heartbeat time to live."""
        return self._subject_push_heartbeat_ttl
    
    @subject_push_heartbeat_ttl.setter
    def subject_push_heartbeat_ttl(self, subject_push_heartbeat_ttl: "int"):
        subject_push_heartbeat_ttl = int(subject_push_heartbeat_ttl)
        if not isinstance(subject_push_heartbeat_ttl, int):
            raise TypeError("'subject_push_heartbeat_ttl' must be of type int")
        self._subject_push_heartbeat_ttl = subject_push_heartbeat_ttl

    @property
    def subject_push_timeout(self) -> "int":
        """The subject push timeout."""
        return self._subject_push_timeout
    
    @subject_push_timeout.setter
    def subject_push_timeout(self, subject_push_timeout: "int"):
        subject_push_timeout = int(subject_push_timeout)
        if not isinstance(subject_push_timeout, int):
            raise TypeError("'subject_push_timeout' must be of type int")
        self._subject_push_timeout = subject_push_timeout

    @property
    def integration_manager_pub_sndhwm(self) -> "int":
        """The integration manager publish high water mark."""
        return self._integration_manager_pub_sndhwm
    
    @integration_manager_pub_sndhwm.setter
    def integration_manager_pub_sndhwm(self, integration_manager_pub_sndhwm: "int"):
        integration_manager_pub_sndhwm = int(integration_manager_pub_sndhwm)
        if not isinstance(integration_manager_pub_sndhwm, int):
            raise TypeError("'integration_manager_pub_sndhwm' must be of type int")
        self._integration_manager_pub_sndhwm = integration_manager_pub_sndhwm

    @property
    def integration_manager_pull_rcvhwm(self) -> "int":
        """The integration manager pull high water mark."""
        return self._integration_manager_pull_rcvhwm
    
    @integration_manager_pull_rcvhwm.setter
    def integration_manager_pull_rcvhwm(self, integration_manager_pull_rcvhwm: "int"):
        integration_manager_pull_rcvhwm = int(integration_manager_pull_rcvhwm)
        if not isinstance(integration_manager_pull_rcvhwm, int):
            raise TypeError("'integration_manager_pull_rcvhwm' must be of type int")
        self._integration_manager_pull_rcvhwm = integration_manager_pull_rcvhwm

    @property
    def worker_timeout(self) -> "int":
        """The worker pull timeout."""
        return self._worker_timeout
    
    @worker_timeout.setter
    def worker_timeout(self, worker_timeout: "int"):
        worker_timeout = int(worker_timeout)
        if not isinstance(worker_timeout, int):
            raise TypeError("'worker_timeout' must be of type int")
        self._worker_timeout = worker_timeout