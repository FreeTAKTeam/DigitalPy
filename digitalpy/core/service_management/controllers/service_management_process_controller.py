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
import multiprocessing

from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.service_management.domain.service_description import ServiceDescription
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

from ..configuration.service_management_constants import SERVICE_WAIT_TIME


class ServiceManagementProcessController(Controller):
    """ Service Management Process Controller class. Responsible for handling all operations on
    a service's underlying process.
    """

    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper,
                 configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)

    def start_process(self, service: ServiceDescription, process_class: DigitalPyService):
        """
        Starts a new process for the given service using the provided process class.

        Args:
            service (ServiceDescription): The service description object.
            process_class (DigitalPyService): The process class to be used for starting the service.

        Raises:
            ChildProcessError: If the service fails to start or if post-processing fails.

        Returns:
            None
        """
        try:
            process = multiprocessing.Process(
                target=process_class.start,
                args=(
                    ObjectFactory.get_instance("factory"),
                    ObjectFactory.get_instance("tracingprovider"),
                    service.host,
                    service.port
                )
            )
            process.start()
        except Exception as e:
            raise ChildProcessError("Service failed to start") from e
        try:
            service.pid = process.pid
            if process.is_alive():
                service.process = process
            else:
                raise ChildProcessError("Service failed to start")
        except Exception as e:
            process.terminate()
            raise ChildProcessError(
                "Service post-processing failed " + str(e)) from e

    def stop_process(self, service: ServiceDescription):
        """
        Stops the specified service process.

        Args:
            service (ServiceDescription): The service to stop.

        Raises:
            ChildProcessException: If the service fails to stop.

        """
        try:
            service.process.join(SERVICE_WAIT_TIME)

            # if the process is still alive, terminate it
            if service.process.is_alive():
                service.process.terminate()
                service.process.join()

            else:
                return
        except Exception as e:
            raise ChildProcessError("Service failed to stop") from e
