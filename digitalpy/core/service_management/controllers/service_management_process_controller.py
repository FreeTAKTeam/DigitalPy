"""
Contains the ServiceManagementProcessController 
class, which is responsible for managing the lifecycle of services in the application. 
This includes starting and stopping service processes.

The class inherits from the Controller class and overrides its methods to provide specific 
functionality for service management. The start_process method is used to start a new service 
process, while the stop_process method is used to stop a running service process.

The ServiceManagementProcessController class uses the multiprocessing module to manage service 
processes,  and handles any exceptions that may occur during the start or stop operations. 
It also uses the ObjectFactory class to get instances of required objects, and the 
ServiceDescription class to describe the services to be managed.

The file also imports several other modules and classes that are used in the 
ServiceManagementProcessController class, including Request, Response, ActionMapper, Configuration, 
DigitalPyService, and SERVICE_WAIT_TIME.
"""

from multiprocessing import Process
from digitalpy.core.service_management.domain.model.service_status_enum import (
    ServiceStatusEnum,
)
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.main.controller import Controller
from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)

from ..configuration.service_management_constants import SERVICE_WAIT_TIME


class ServiceManagementProcessController(Controller):
    """Service Management Process Controller class. Responsible for handling all operations on
    a service's underlying process.
    """

    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ):
        super().__init__(request, response, sync_action_mapper, configuration)

    def start_process(self, service: DigitalPyService):
        """
        Starts a new process for the given service using the provided process class.

        Args:
            service (DigitalPyService): The service object instance.

        Raises:
            ChildProcessError: If the service fails to start or if post-processing fails.
        """
        if service.process is None:
            service.process = Process(
                target=service.start,
                args=(
                    ObjectFactory.get_instance("factory"),
                    ObjectFactory.get_instance("TracingProvider"),
                    SingletonConfigurationFactory.get_instance(),
                ),
            )
        try:
            service.process.start()
        except Exception as e:
            service.status = ServiceStatusEnum.ERROR.value
            raise ChildProcessError("Service failed to start") from e
        try:
            if not service.process.is_alive():
                service.status = ServiceStatusEnum.ERROR.value
                raise ChildProcessError("Service failed to start")
        except Exception as e:
            service.process.terminate()
            service.status = ServiceStatusEnum.ERROR.value
            raise ChildProcessError("Service post-processing failed " + str(e)) from e
        service.status = ServiceStatusEnum.RUNNING.value
        return service

    def stop_process(self, service: DigitalPyService):
        """
        Stops the specified service process.

        Args:
            service (DigitalPyService): The service to stop.
        """
        try:
            service.process.join(SERVICE_WAIT_TIME)

            # if the process is still alive, terminate it
            if service.process.is_alive():
                service.process.terminate()
                service.process.join()

            service.process = None

            service.configuration.status = ServiceStatusEnum.STOPPED.value
        except Exception as e:
            service.status = ServiceStatusEnum.ERROR.value
            raise ChildProcessError("Service failed to stop") from e
