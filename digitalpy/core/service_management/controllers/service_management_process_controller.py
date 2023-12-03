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

class ServiceManagementProcessController(Controller):
    """ Service Management Process Controller class. Responsible for handling all operations on
    a service's underlying process.
    """

    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def start_process(self, service: ServiceDescription):
        """Starts a service's underlying process.

        Args:
            service (ServiceDescription): The service to start.
        """
        process_class: DigitalPyService = ObjectFactory.get_instance(service.id)
        process = multiprocessing.Process(target=process_class.start, args=(ObjectFactory.get_instance("factory"), ObjectFactory.get_instance("tracingprovider")))
        process.start()
        service.pid = process.pid
        if service.process.is_alive():
            service.process = process
        else:
            raise Exception("Service failed to start")