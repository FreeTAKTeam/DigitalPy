from argparse import Action
from config.action_key import ActionKey
from model.application_event import ApplicationEvent
from config.impl.config_action_key_provider import ConfigActionKeyProvider
from config.configuration import Configuration
from core.event_manager import EventManager
from request import Request
from response import Response
from routing.action_mapper import ActionMapper

from core.object_factory import ObjectFactory


class DefaultActionMapper(ActionMapper):
	#
	#Constructor
	#@param session
	#@param permissionManager
	#@param eventManager
	#@param formatter
	#@param configuration
	#
	def __init__(self, event_manager: EventManager,
					configuration: Configuration):
		self.eventManager = event_manager
		self.configuration = configuration
		self.is_finished = False
	

	#
	#@see ActionMapper.processAction()
	#
	def process_action(self, request: Request, response: Response):
		self.eventManager.dispatch(ApplicationEvent.NAME, ApplicationEvent(
						ApplicationEvent.BEFORE_ROUTE_ACTION, request))
		actionKeyProvider = ConfigActionKeyProvider(self.configuration, 'actionmapping')

		referrer = request.get_sender()
		context = request.get_context()
		action = request.get_action()
		response.set_sender(referrer)
		response.set_context(context)
		response.set_action(action)
		#response.set_format(request.get_response_format())

		# get best matching action key from inifile
		actionKey = ActionKey.get_best_match(actionKeyProvider, referrer, context, action)

		if len(actionKey) == 0 :
			# return, if action key is not defined
			return
		

		# get next controller
		controllerClass = None
		controllerDef = self.configuration.get_value(actionKey, 'actionmapping')
		if len(controllerDef) == 0:
			self.logger.error("No controller found for best action key "+actionKey+
							". Request was referrer?context?action")
			Exception(request, response)
		

		# check if the controller definition contains a method besides the class name
		controllerMethod = None
		if '.' in controllerDef:
			controller_def_list = controllerDef.split('.')
			controllerClass = '.'.join(controller_def_list[:-1])
			controllerMethod = controller_def_list[-1]
		else:
			controllerClass = controllerDef

		# instantiate controller
		controllerObj = ObjectFactory.get_instance_of(controllerClass)

		# everything is right in place, start processing
		
  		#self.formatter.deserialize(request)

		# initialize controller
		self.eventManager.dispatch(ApplicationEvent.NAME, ApplicationEvent(
						ApplicationEvent.BEFORE_INITIALIZE_CONTROLLER, request, response, controllerObj))
		controllerObj.initialize(request, response)

		# execute controller
		self.eventManager.dispatch(ApplicationEvent.NAME, ApplicationEvent(
						ApplicationEvent.BEFORE_EXECUTE_CONTROLLER, request, response, controllerObj))
		controllerObj.execute(controllerMethod)
		self.eventManager.dispatch(ApplicationEvent.NAME, ApplicationEvent(
						ApplicationEvent.AFTER_EXECUTE_CONTROLLER, request, response, controllerObj))

		# return if we are finished
		if self.is_finished:
			#self.formatter.serialize(response)
			return None
		

		# check if an action key exists for the return action
		nextActionKey = ActionKey.get_best_match(actionKeyProvider, controllerClass,
						response.get_context(), response.get_action())

		# terminate
		# - if there is no next action key or
		# - if the next action key is the same as the previous one (to prevent recursion)
		terminate = len(nextActionKey) == 0 or actionKey == nextActionKey
		if terminate:
			# stop processing
			#self.formatter.serialize(response)
			self.isFinished = True
			return None

		# set the request based on the result
		nextRequest = ObjectFactory.get_new_instance('request')
		nextRequest.set_sender(controllerClass)
		nextRequest.set_context(response.get_context())
		nextRequest.set_action(response.get_action())
		#nextRequest.set_format(response.get_format())
		nextRequest.set_values(response.get_values())
		#nextRequest.set_errors(response.get_errors())
		#nextRequest.set_response_format(request.get_response_format())
		self.process_action(nextRequest, response)