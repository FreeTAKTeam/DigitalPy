from datetime import datetime
from digitalpy.core.domain.node import Node
from digitalpy.core.health.domain.service_health_category import ServiceHealthCategory


class ServiceHealth(Node):
    """service health class"""

    def __init__(self, model_configuration=None, model=None, oid=None,
                 node_type="service_health") -> None:
        super().__init__(node_type, model_configuration=model_configuration,
                         model=model, oid=oid)  # type: ignore
        # id of the service
        self._service_id: str
        # the status of the service
        self._status: ServiceHealthCategory
        # the time that the health was recorded
        self._timestamp: datetime
        # the percentage of errors per request
        self._error_percentage: float

    @property
    def average_request_time(self) -> float:
        """get the average request time of the service

        Returns:
            float: the average request time of the service
        """
        return self._average_request_time

    @average_request_time.setter
    def average_request_time(self, average_request_time: float):
        """set the average request time of the service

        Args:
            average_request_time (float): the average request time of the service
        """
        if not isinstance(average_request_time, float) and not isinstance(average_request_time, int):
            raise TypeError(
                "'average_request_time' must be an instance of float")
        self._average_request_time = float(average_request_time)

    @property
    def error_percentage(self) -> float:
        """get the error percentage of the service

        Returns:
            float: the error percentage of the service
        """
        return self._error_percentage

    @error_percentage.setter
    def error_percentage(self, error_percentage: float):
        """set the error percentage of the service

        Args:
            error_percentage (float): the error percentage of the service
        """
        if not isinstance(error_percentage, float) and not isinstance(error_percentage, int):
            raise TypeError("'error_percentage' must be an instance of float")
        self._error_percentage = float(error_percentage)

    @property
    def service_id(self) -> str:
        """get the service id of the service

        Returns:
            str: the service id of the service
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id: str):
        """set the service id of the service

        Args:
            service_id (str): the service id of the service
        """
        if not isinstance(service_id, str):
            raise TypeError("'service_id' must be an instance of str")
        self._service_id = service_id

    @property
    def status(self) -> ServiceHealthCategory:
        """get the status of the service

        Returns:
            str: the status of the service
        """
        return self._status

    @status.setter
    def status(self, status: ServiceHealthCategory):
        """set the status of the service

        Args:
            status (str): the status of the service
        """
        if not isinstance(status, ServiceHealthCategory):
            raise TypeError(
                "'status' must be an instance of ServiceHealthCategory")
        self._status = status

    @property
    def timestamp(self) -> datetime:
        """get the timestamp of the service

        Returns:
            datetime: the timestamp of the service
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """set the timestamp of the service

        Args:
            timestamp (datetime): the timestamp of the service
        """
        if not isinstance(timestamp, datetime):
            raise TypeError("'timestamp' must be an instance of datetime")
        self._timestamp = timestamp

    def __str__(self) -> str:
        return f"ServiceHealth(service_id={self.service_id}, status={self.status}, timestamp={self.timestamp}, error_percentage={self.error_percentage}, average_request_time={self.average_request_time})"
