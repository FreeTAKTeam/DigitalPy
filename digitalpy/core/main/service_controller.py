from .controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory

class ServiceController(Controller):

    def execute_sub_action(self, action):
        """make a request to the zmanager

        Args:
            action (str): the action key to be sent
            values (Dict, optional): the values to be sent in the reques. Defaults to {}.
            synchronous (bool, optional): whether or not to wait for a response from the zmanager. Defaults to True.
            service_id (str, optional): what service to share the request response with. Defaults to None.
        Returns:
            Response: the response coming from the the zmanager
        Raises:
            ValueError: raised when synchronous is true and service_id is neither None or rest api service id as this
                            will result in an undefined state where we are waiting for a response that will never come
        """
        https_tak_api_service = ObjectFactory.get_instance("HTTPSTakAPIService")
        service_id_different = service_id is not None and https_tak_api_service.service_id != service_id
        if synchronous == True and service_id_different:
            raise ValueError("synchronous is true and service_id is neither None or rest api service id,\
                              this will result in an undefined state where we are waiting for a response that will never come")

        # request to get repeated messages
        request: Request = ObjectFactory.get_new_instance("request")
        request.set_action(action)
        request.set_sender(https_tak_api_service.__class__.__name__.lower())
        request.set_format("pickled")
        request.set_values(values)
        https_tak_api_service.subject_send_request(request, APPLICATION_PROTOCOL, service_id)
        if synchronous == True:
            response = https_tak_api_service.retrieve_response(request.get_id())
            return response