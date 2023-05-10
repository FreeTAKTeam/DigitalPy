import logging
from digitalpy.core.digipy_configuration.action_key import ActionKey
from digitalpy.core.persistence.application_event import ApplicationEvent
from digitalpy.core.digipy_configuration.impl.config_action_key_provider import ConfigActionKeyProvider
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.event_manager import EventManager
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper

from digitalpy.core.main.object_factory import ObjectFactory


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
    ):
        self.eventManager = event_manager
        self.configuration = configuration
        self.is_finished = False
        self.tracing_provider = None
        self.logger = logging.getLogger("DefaultActionMapper")

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

    def process_action(self, request: Request, response: Response)-> None:
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
        actionKeyProvider = ConfigActionKeyProvider(self.configuration, "actionmapping")

        referrer = request.get_sender()
        context = request.get_context()
        action = request.get_action()
        response.set_sender(referrer)
        response.set_context(context)
        response.set_action(action)
        # response.set_format(request.get_response_format())

        # get best matching action key from inifile
        actionKey = ActionKey.get_best_match(
            actionKeyProvider, referrer, context, action
        )

        if len(actionKey) == 0:
            # return, if action key is not defined
            return

        # get next controller
        controllerClass = None
        controllerDef = self.configuration.get_value(actionKey, "actionmapping")
        if len(controllerDef) == 0:
            self.logger.error(
                "No controller found for best action key "
                + actionKey
                + ". Request was referrer?context?action"
            )
            raise Exception("No controller found for best action key "+ actionKey)

        # check if the controller definition contains a method besides the class name
        controllerMethod = None
        if "." in controllerDef:
            controller_def_list = controllerDef.split(".")
            controllerClass = ".".join(controller_def_list[:-1])
            controllerMethod = controller_def_list[-1]
        else:
            controllerClass = controllerDef

        # instantiate controller
        controllerObj = ObjectFactory.get_instance_of(controllerClass, dynamic_configuration={"request": request, "response": response})

        # everything is right in place, start processing

        # self.formatter.deserialize(request)

        # initialize controller
        self.eventManager.dispatch(
            ApplicationEvent.NAME,
            ApplicationEvent(
                ApplicationEvent.BEFORE_INITIALIZE_CONTROLLER,
                request,
                response,
                controllerObj,
            ),
        )
        controllerObj.initialize(request, response)

        # execute controller
        self.eventManager.dispatch(
            ApplicationEvent.NAME,
            ApplicationEvent(
                ApplicationEvent.BEFORE_EXECUTE_CONTROLLER,
                request,
                response,
                controllerObj,
            ),
        )
        try:
            controllerObj.execute(controllerMethod)
        except Exception as e:
            raise e
        self.eventManager.dispatch(
            ApplicationEvent.NAME,
            ApplicationEvent(
                ApplicationEvent.AFTER_EXECUTE_CONTROLLER,
                request,
                response,
                controllerObj,
            ),
        )

        # return if we are finished
        if self.is_finished:
            # self.formatter.serialize(response)
            return None

        # check if an action key exists for the return action
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
