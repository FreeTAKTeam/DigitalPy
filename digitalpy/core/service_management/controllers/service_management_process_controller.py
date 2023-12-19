import multiprocessing

from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.service_management.domain.service_description import ServiceDescription
from digitalpy.core.service_management.domain.service_status import ServiceStatus
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

# time to wait until a service is manually terminated
SERVICE_WAIT_TIME = 10

class ServiceManagementProcessController(Controller):
    """ Service Management Process Controller class. Responsible for handling all operations on
    a service's underlying process.
    """

    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def start_process(self, service: ServiceDescription, process_class: DigitalPyService):
        """Starts a service's underlying process.

        Args:
            service (ServiceDescription): The service to start.
        """
        try:
            process = multiprocessing.Process(target=process_class.start, args=(ObjectFactory.get_instance("factory"), ObjectFactory.get_instance("tracingprovider"), service.host, service.port))
            process.start()
        except Exception as e:
            raise Exception("Service failed to start: " + str(e))
        try:
            service.pid = process.pid
            if process.is_alive():
                service.process = process
            else:
                raise Exception("Service failed to start")
        except Exception as e:
            process.terminate()
            raise Exception("Service post-processing failed " + str(e))
        
    def stop_process(self, service: ServiceDescription):
        try:
            service.process.join(SERVICE_WAIT_TIME)
            
            # if the process is still alive, terminate it
            if service.process.is_alive():
                service.process.terminate()
                service.process.join()
            
            else:
                return
        except Exception as e:
            raise Exception("Service failed to stop: " + str(e))