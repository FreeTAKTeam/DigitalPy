import logging
from typing import TYPE_CHECKING
from digitalpy.core.main.controller import Controller
from digitalpy.core.digipy_configuration.configuration.digipy_configuration_constants import (
    ACTION_MAPPING_SECTION,
)
from digitalpy.core.digipy_configuration.action_key import ActionKey
from digitalpy.core.persistence.application_event import ApplicationEvent
from digitalpy.core.digipy_configuration.impl.config_action_key_provider import (
    ConfigActionKeyProvider,
)
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.main.event_manager import EventManager
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.action_key_controller import (
    ActionKeyController,
)

from digitalpy.core.main.object_factory import ObjectFactory

if TYPE_CHECKING:
    from digitalpy.core.IAM.IAM_facade import IAM


class DefaultActionMapper(ActionMapper):
    #
    # Constructor
    # @param session
    # @param permissionManager
    # @param eventManager
    # @param formatter
    # @param configuration
    #
    def __init__(
        self,
        event_manager: EventManager,
        configuration: Configuration,
        iam: "IAM" = None,
    ):
        self.eventManager = event_manager
        self.configuration = configuration
        self.is_finished = False
        self.tracing_provider = None
        self.logger = logging.getLogger("DefaultActionMapper")
        self.logger.setLevel(logging.DEBUG)
        self.iam: "IAM" = iam
        self.action_key_controller: ActionKeyController = ObjectFactory.get_instance(
            "ActionKeyController"
        )

    #
    # @see ActionMapper.processAction()
    #
    def initialize_tracing(self):
        try:
            # new instance used because the contents of tracing_provider cant be serialized between
            # processes and so shouldnt be persisted in the factory hance we have custom handling
            # to avoid duplication of the tracing provider
            self.tracing_provider = ObjectFactory.get_new_instance("tracingprovider")
            ObjectFactory.register_instance(
                "tracingproviderinstance", self.tracing_provider
            )
        except Exception as e:
            pass

    def process_action(self, request: Request, response: Response) -> None:
        # TODO break up this method
        """this is the main method for routing and processing requests within the action mapper

        Args:
            request (Request): the request containing an action to be routed
            response (Response): the response to be filled with response data from the component

        Raises:
            Exception

        Returns:
            None: return a none
        """
        # this is added for the sake of the latter use of multiprocessing
        if not self.tracing_provider:
            self.initialize_tracing()

        self.eventManager.dispatch(
            ApplicationEvent.NAME,
            ApplicationEvent(ApplicationEvent.BEFORE_ROUTE_ACTION, request),
        )
        actionKeyProvider = ConfigActionKeyProvider(
            self.configuration, ACTION_MAPPING_SECTION
        )

        referrer: str = request.get_sender()
        context: str = request.get_context()
        action: str = request.get_action()
        response.set_id(request.get_id())
        response.set_sender(referrer)
        response.set_context(context)
        response.set_action(action)
        # response.set_format(request.get_response_format())

        # get best matching action key from inifile
        actionKey = self.action_key_controller.resolve_action_key(request.action_key)

        # authenticate user
        if not self.authorize_operation(request, action_key=actionKey):
            raise PermissionError("User not authorized to perform this operation")

        # get next controller
        controllerClass, controllerMethod, controller_obj = self._get_controller(
            request, response, actionKey.target
        )

        # everything is right in place, start processing

        # self.formatter.deserialize(request)

        # initialize controller
        self._execute_operation(request, response, controllerMethod, controller_obj)

        # return if we are finished
        if self.is_finished:
            # self.formatter.serialize(response)
            return None

        # check if an action key exists for the return action
        return self._get_next_action(
            response, actionKeyProvider, actionKey, controllerClass
        )

    def _get_next_action(self, response, actionKeyProvider, actionKey, controllerClass):
        """This has been left to maintain back compatability with the previous implementation before the addition of action flows"""
        nextActionKey = ActionKey.get_best_match(
            actionKeyProvider,
            controllerClass,
            response.get_context(),
            response.get_action(),
        )

        # terminate
        # - if there is no next action key or
        # - if the next action key is the same as the previous one (to prevent recursion)
        terminate = len(nextActionKey) == 0 or actionKey == nextActionKey
        if terminate:
            # stop processing
            # self.formatter.serialize(response)
            self.isFinished = True
            return None

        # set the request based on the result
        nextRequest = ObjectFactory.get_new_instance("request")
        nextRequest.set_sender(controllerClass)
        nextRequest.set_context(response.get_context())
        nextRequest.set_action(response.get_action())
        nextRequest.set_format(response.get_format())
        nextRequest.set_values(response.get_values())
        # nextRequest.set_errors(response.get_errors())
        # nextRequest.set_response_format(request.get_response_format())
        self.process_action(nextRequest, response)

    def _execute_operation(self, request, response, controllerMethod, controller_obj):
        self.eventManager.dispatch(
            ApplicationEvent.NAME,
            ApplicationEvent(
                ApplicationEvent.BEFORE_INITIALIZE_CONTROLLER,
                request,
                response,
                controller_obj,
            ),
        )
        controller_obj.initialize(request, response)

        # execute controller
        self.eventManager.dispatch(
            ApplicationEvent.NAME,
            ApplicationEvent(
                ApplicationEvent.BEFORE_EXECUTE_CONTROLLER,
                request,
                response,
                controller_obj,
            ),
        )
        try:
            self.logger.debug(
                "executing method %s on controller %s",
                str(controllerMethod),
                str(type(controller_obj)),
            )
            controller_obj.execute(controllerMethod)
        except Exception as e:
            raise e
        self.eventManager.dispatch(
            ApplicationEvent.NAME,
            ApplicationEvent(
                ApplicationEvent.AFTER_EXECUTE_CONTROLLER,
                request,
                response,
                controller_obj,
            ),
        )

    def _get_controller(self, request, response, actionKeyTarget: str):
        controllerClass = None
        controllerDef = actionKeyTarget
        if len(controllerDef) == 0:
            self.logger.error(
                "No controller found for best action key "
                + actionKeyTarget
                + ". Request was referrer?context?action"
            )
            raise Exception(
                "No controller found for best action key " + actionKeyTarget
            )

        # check if the controller definition contains a method besides the class name
        controllerMethod = None
        if "." in controllerDef:
            controller_def_list = controllerDef.split(".")
            controllerClass = ".".join(controller_def_list[:-1])
            controllerMethod = controller_def_list[-1]
        else:
            controllerClass = controllerDef

        # instantiate controller
        controller_obj: Controller = ObjectFactory.get_instance_of(
            controllerClass,
            dynamic_configuration={"request": request, "response": response},
        )
        return controllerClass, controllerMethod, controller_obj

    def authorize_operation(self, request: Request, action_key: ActionKey) -> bool:
        """this method is responsible for authorizing the operation with the IAM component"""
        if not self.iam:
            self.iam: "IAM" = ObjectFactory.get_instance("IAM")

        if not self.iam.filter_action(
            request=request, action_key=action_key, user=request.get_value("client")
        ):
            return False

        else:
            return True
