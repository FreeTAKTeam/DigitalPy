from digitalpy.core.domain.node import Node
from digitalpy.core.parsing.load_configuration import ModelConfiguration

class ServiceManagementConfiguration(Node):
    """ This class defines the basic configuration of a service management in a digitalpy environment.
    Primarily, it contains the list of services that are managed by the service management. As a configuration
    object, it is expected to be initialized dynamically by the configuration factory. An iniconfiguration
    which could be used to initialize this object is shown below:
    [ServiceManagementConfiguration]
    __class = digitalpy.core.service_management.domain.service_management_configuration.ServiceManagementConfiguration
    services = [digitalpy.core_api]
    
    Attributes:
        services (list[str]): The list of services.
    """
    
    def __init__(self, model_configuration=ModelConfiguration(), model={}, node_type = "service_management_configuration", oid=None) -> None:
        super().__init__(model_configuration=model_configuration, model=model, node_type=node_type, oid=oid)
        self._services: list[str]

    @property
    def services(self) -> list[str]:
        """
        Get the list of services.
        
        Returns:
            list[str]: The list of services.
        """
        return self._services

    @services.setter
    def services(self, value: list[str]) -> None:
        """
        Set the list of services.
        
        Args:
            value (list[str]): The list of services.
        """
        self._services = value
