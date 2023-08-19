from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

class ServiceManagementCommunicationController(Controller):

    def __init__(self, service_id: str, service_key, application_protocol: str, request: Request, response: Response, action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, action_mapper, configuration)
        self._service_id = service_id
        self._service_key = service_key
        self._application_protocol = application_protocol
        
    def set_service(self, service_id):
        self._service_id = service_id

    def set_application_protocol(self, application_protocol):
        self._application_protocol = application_protocol

    def make_request(self, action: str, context: str = "", values: dict={}, target_service_name: str=None, synchronous: bool=True):
        """this function enables a service to make requests

        Args:
            action (str): the action
            recipients (List[str]): the id's of all clients to which this message should be sent accross services
            
            origin_service_name (List[str]): the id's of all services to which the message should be sent

        Returns:
            _type_: _description_
        """
        print("making request to service: " + str(self._service_id) + " with action: " + str(action) + " and context: " + str(context) + " and values: " + str(values))
        if target_service_name is None:
            target_service_name = self._service_id

        service_instance = ObjectFactory.get_instance(self._service_key)
        service_id_different = self._service_id is not None and service_instance.service_id != self._service_id
        if synchronous == True and service_id_different:
            raise ValueError("synchronous is true and service_id is neither None or rest api service id,\
                              this will result in an undefined state where we are waiting for a response that will never come")

        # request to get repeated messages
        request: Request = ObjectFactory.get_new_instance("request")
        request.set_action(action)
        request.set_context(context)
        request.set_sender(service_instance.__class__.__name__.lower())
        request.set_format("pickled")
        request.set_values(values)
        service_instance.subject_send_request(request, self._application_protocol, target_service_name)
        if synchronous == True:
            response = service_instance.retrieve_response(request.get_id())
            return response
