from abc import ABC
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

# 1. The controller is initialized with the request and response objects
# 2. The controller is initialized with the action mapper
# 3. The controller is initialized with the configuration
# 4. The initialize method is called with the request and response objects
# 5. The request and response objects are set

class Controller(ABC):
    request = None
    response = None
    logger = None
    session = None
    persistence_facade = None
    permission_manager = None
    action_mapper = None
    localization = None
    message = None
    configuration = None

    started_transaction = False

    def __init__(
        self,
        request: Request,
        response: Response,
        action_mapper: ActionMapper,
        configuration: Configuration,
    ):
        self.action_mapper = action_mapper
        self.configuration = configuration

    def initialize(self, request: Request, response: Response):
        response.set_sender(self.__class__.__name__)

        self.request = request
        self.response = response

    def validate(self):
        return True

    def execute(self, method=None):
        validation_failed = False
        if not self.validate():
            validation_failed = True
        if not validation_failed:
            try:
                self.do_execute(method)
                self.end_transaction()
            except Exception as ex:
                self.response.add_error(ex)
                self.response.set_status(ex.code)
                self.end_transaction(False)
        errors = self.request.get_errors().join(self.response.get_errors())
        if len(errors) > 0:
            error = errors.pop()
            self.response.set_value("error_code", error.code)
            self.response.set_value("error_message", error.message)

    def do_execute(self):
        raise NotImplementedError

    def get_request(self):
        return self.request

    def get_response(self):
        return self.response

    def execute_sub_action(self, action):
        cur_request = self.get_request()
        cur_response = self.get_response()
        sub_request = ObjectFactory.get_new_instance("request")
        sub_request.set_sender(self.__class__.__name__)
        sub_request.set_context(cur_request.get_context())
        sub_request.set_action(action)
        sub_request.set_values(cur_request.get_values().copy())
        sub_request.set_format(cur_request.get_format())
        sub_response = ObjectFactory.get_new_instance("response")
        sub_response.set_format(cur_response.get_format())
        # if statement to check if the async action mapper is being used
        # in which case we need to get the response
        if hasattr(self.action_mapper, "get_response"):
            listener = self.action_mapper.process_action(
                sub_request, sub_response, return_listener=True
            )
            self.action_mapper.get_response(sub_response, sub_request, listener)
        else:
            self.action_mapper.process_action(sub_request, sub_response)
        return sub_response
