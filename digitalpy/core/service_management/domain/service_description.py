from datetime import datetime as dt
from multiprocessing import Process
from digitalpy.core.domain.node import Node
from digitalpy.core.service_management.domain.service_status import ServiceStatus

class ServiceDescription(Node):
    def __init__(self, node_type = "service_description", oid=None) -> None:
        super().__init__(node_type, oid=oid)
        # the pid of the service, changing depending on the status of the service
        self._pid: int = None  # type: ignore
        # the id of the service (must be unique), consistent throughout the lifetime of the service, this must be in the form, <component_name>.<service_name>
        self._id: str = None  # type: ignore
        # the protocol of the service
        self._protocol: str = None  # type: ignore
        # the status of the service in it's lifecycle
        self._status: ServiceStatus = None  # type: ignore
        # the description of the service
        self._description: str = None  # type: ignore
        # the human readable name of the service, should be unique but not required.
        self._name: str = None  # type: ignore
        # when the last message from the service was received
        self._last_message_time: dt = None  # type: ignore
        # when the service was started
        self._start_time: dt = None  # type: ignore
        # the process of the service (if it is running)
        self._process: Process = None  # type: ignore
        # host address if the process is attached to a network
        self._host: str = None  # type: ignore
        # port if the process is attached to a network
        self._port: int = None  # type: ignore
        # network interface if the process is attached to a network
        self._network_interface: str = None  # type: ignore

    @property
    def network_interface(self) -> str:
        """get the network interface of the service

        Returns:
            str: the network interface of the service
        """
        return self._network_interface
    
    @network_interface.setter
    def network_interface(self, network_interface: str):
        """set the network interface of the service

        Args:
            network_interface (str): the network interface of the service

        Raises:
            TypeError: if network_interface is not a string
        """
        if not isinstance(network_interface, str):
            raise TypeError("'network_interface' must be a string")
        
        self._network_interface = network_interface

    @property
    def host(self) -> str:
        """get the host of the service

        Returns:
            str: the host of the service
        """
        return self._host
    
    @host.setter
    def host(self, host: str):
        """set the host of the service

        Args:
            host (str): the host of the service

        Raises:
            TypeError: if host is not a string
        """
        if not isinstance(host, str):
            raise TypeError("'host' must be a string")
        self._host = host

    @property
    def port(self) -> int:
        """get the port of the service

        Returns:
            int: the port of the service
        """
        return self._port
    
    @port.setter
    def port(self, port: int):
        """set the port of the service

        Args:
            port (int): the port of the service

        Raises:
            TypeError: if port is not an integer
        """
        if not isinstance(port, int):
            raise TypeError("'port' must be an integer")
        self._port = port

    @property
    def process(self) -> Process:
        """get the process of the service

        Returns:
            Process: the process of the service
        """
        return self._process
    
    @process.setter
    def process(self, process: Process):
        """set the process of the service

        Args:
            process (Process): the process of the service
        """
        if not isinstance(process, Process):
            raise TypeError("'process' must be an instance of Process")
        if not process.is_alive():
            raise ValueError("'process' must be alive")
        if self._process != None:
            raise ValueError("'process' must be None to set to a new value")
        self._process = process

    @property
    def start_time(self) -> dt:
        """get the start time of the service

        Returns:
            dt: the start time of the service
        """
        return self._start_time
    
    @start_time.setter
    def start_time(self, start_time: dt):
        """set the start time of the service

        Args:
            start_time (dt): the start time of the service
        """
        if not isinstance(start_time, dt):
            raise TypeError("'start_time' must be an instance of datetime")
        self._start_time = start_time

    @property
    def last_message_time(self) -> dt:
        """get the last message time of the service

        Returns:
            dt: the last message time of the service
        """
        return self._last_message_time

    @last_message_time.setter
    def last_message_time(self, last_message_time: dt):
        """set the last message time of the service

        Args:
            last_message_time (dt): the last message time of the service
        """
        if not isinstance(last_message_time, dt):
            raise TypeError("'last_message_time' must be an instance of datetime")
        self._last_message_time = last_message_time

    @property
    def pid(self) -> int:
        """get the pid of the service

        Returns:
            int: the pid of the service
        """
        return self._pid
    
    @pid.setter
    def pid(self, pid: int):
        """set the pid of the service, this should only be done by the service manager
        and only the in the event the service is restarted.

        Args:
            pid (int): the pid of the service
        """
        if not isinstance(pid, int):
            raise TypeError("'pid' must be an integer")
        self._pid = pid

    @property
    def id(self) -> str:
        """get the id of the service

        Returns:
            str: the id of the service
        """
        return self._id
    
    @id.setter
    def id(self, id: str):
        """set the id of the service.

        Args:
            id (str): the id of the service
        """
        if not isinstance(id, str):
            raise TypeError("'id' must be a string")
        self._id = id

    @property
    def protocol(self) -> str:
        """get the protocol of the service

        Returns:
            str: the protocol of the service
        """
        return self._protocol
    
    @protocol.setter
    def protocol(self, protocol: str):
        """set the protocol of the service

        Args:
            protocol (str): the protocol of the service
        """
        if not isinstance(protocol, str):
            raise TypeError("'protocol' must be a string")
        
        self._protocol = protocol

    @property
    def status(self) -> ServiceStatus:
        """get the status of the service

        Returns:
            ServiceStatus: the status of the service
        """
        return self._status
    
    @status.setter
    def status(self, status: ServiceStatus):
        """set the status of the service

        Args:
            status (ServiceStatus): the status of the service
        """
        if not isinstance(status, ServiceStatus):
            raise TypeError("'status' must be an instance of ServiceStatus")
        
        self._status = status

    @property
    def description(self) -> str:
        """get the description of the service

        Returns:
            str: the description of the service
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """set the description of the service

        Args:
            description (str): the description of the service
        """
        if not isinstance(description, str):
            raise TypeError("'description' must be a string")
        
        self._description = description

    @property
    def name(self) -> str:
        """get the name of the service

        Returns:
            str: the name of the service
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """set the name of the service

        Args:
            name (str): the name of the service
        """
        if not isinstance(name, str):
            raise TypeError("'name' must be a string")
        
        self._name = name