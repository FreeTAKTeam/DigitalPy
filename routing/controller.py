from abc import ABC
from routing.action_mapper import ActionMapper
from config.configuration import Configuration

from request import Request
from response import Response

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

    def __init__(self, request: Request, response: Response, action_mapper: ActionMapper, configuration: Configuration):
        pass

    def initialize(self, request: Request, response: Response):
        response.setSender(self)

        self.request = request
        self.response = response

    def validate(self):
        return True

    def execute(self, method = None):
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
            self.response.set_value('error_code', error.code)
            self.response.set_value('error_message', error.message)

    def do_execute(self):
        raise NotImplementedError

    def execute_sub_action(self, action):
        cur_request = self.get_request()
        sub_request = ObjectFactory.get_new_instance('request')
        sub_request.set_sender(self)
        sub_request.set_context(cur_request.get_context())
        sub_request.set_action(action)
        sub_request.set_headers(cur_request.get_headers())
        sub_request.set_values(cur_request.get_values())
        sub_request.setFormat('null')
        sub_request.setResponseFormat('null')
        sub_request = ObjectFactory.get_new_instance()