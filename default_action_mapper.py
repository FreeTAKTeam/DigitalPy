from argparse import Action
from action_key import ActionKey
from application_event import ApplicationEvent
from config_action_key_provider import ConfigActionKeyProvider
from configuration import Configuration
from event_manager import EventManager
from request import Request
from response import Response
from action_mapper import ActionMapper

from object_factory import ObjectFactory


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
	

	#
	#@see ActionMapper.processAction()
	#
	def processAction(self, request: Request, response: Response):
		DefaultActionMapper.eventManager.dispatch(ApplicationEvent.NAME, ApplicationEvent(
						ApplicationEvent.BEFORE_ROUTE_ACTION, request))
		actionKeyProvider = ConfigActionKeyProvider(DefaultActionMapper.configuration, 'actionmapping')

		referrer = request.getSender()
		context = request.getContext()
		action = request.getAction()
		response.setSender(referrer)
		response.setContext(context)
		response.setAction(action)
		response.setFormat(request.getResponseFormat())

		# get best matching action key from inifile
		actionKey = ActionKey.getBestMatch(actionKeyProvider, referrer, context, action)

		if len(actionKey) == 0 :
			# return, if action key is not defined
			return
		

		# get next controller
		controllerClass = None
		controllerDef = DefaultActionMapper.configuration.getValue(actionKey, 'actionmapping')
		if len(controllerDef) == 0:
			self.logger.error("No controller found for best action key "+actionKey+
							". Request was referrer?context?action")
			Exception(request, response)
		

		# check if the controller definition contains a method besides the class name
		controllerMethod = None
		if '.' in controllerDef:
			controller_def_list = controllerDef.split('::')
			controllerClass = controller_def_list[0]
			controllerMethod = controller_def_list[1]
		else:
			controllerClass = controllerDef

		# instantiate controller
		controllerObj = ObjectFactory.getInstanceOf(controllerClass)

		# everything is right in place, start processing
		DefaultActionMapper.formatter.deserialize(request)

		# initialize controller
		DefaultActionMapper.eventManager.dispatch(ApplicationEvent.NAME, ApplicationEvent(
						ApplicationEvent.BEFORE_INITIALIZE_CONTROLLER, request, response, controllerObj))
		controllerObj.initialize(request, response)

		# execute controller
		DefaultActionMapper.eventManager.dispatch(ApplicationEvent.NAME, ApplicationEvent(
						ApplicationEvent.BEFORE_EXECUTE_CONTROLLER, request, response, controllerObj))
		controllerObj.execute(controllerMethod)
		DefaultActionMapper.eventManager.dispatch(ApplicationEvent.NAME, ApplicationEvent(
						ApplicationEvent.AFTER_EXECUTE_CONTROLLER, request, response, controllerObj))

		# return if we are finished
		if DefaultActionMapper.isFinished:
			DefaultActionMapper.formatter.serialize(response)
			return None
		

		# check if an action key exists for the return action
		nextActionKey = ActionKey.getBestMatch(actionKeyProvider, controllerClass,
						response.getContext(), response.getAction())

		# terminate
		# - if there is no next action key or
		# - if the next action key is the same as the previous one (to prevent recursion)
		terminate = len(nextActionKey) == 0 or actionKey == nextActionKey
		if terminate:
			# stop processing
			DefaultActionMapper.formatter.serialize(response)
			DefaultActionMapper.isFinished = True
			return None

		# set the request based on the result
		nextRequest = ObjectFactory.getNewInstance('request')
		nextRequest.setSender(controllerClass)
		nextRequest.setContext(response.getContext())
		nextRequest.setAction(response.getAction())
		nextRequest.setFormat(response.getFormat())
		nextRequest.setValues(response.getValues())
		nextRequest.setErrors(response.getErrors())
		nextRequest.setResponseFormat(request.getResponseFormat())
		DefaultActionMapper.processAction(nextRequest, response)