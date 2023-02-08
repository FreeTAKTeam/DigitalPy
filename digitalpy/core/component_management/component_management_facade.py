from digitalpy.component.impl.default_facade import DefaultFacade
#protectedstart imports ############################################################################
#protectedend ######################################################################################


#protectedstart classDeclaration ###################################################################
class ComponentManagementFacade(DefaultFacade):
#protectedend ######################################################################################




	"""Facade class for the this component. Responsible for handling all public
	routing. Forwards all requests to the internal router.
	WHY:
	<ul>
	<li><b>Isolation</b>: We can easily isolate our code from the complexity of
	a subsystem.</li>
	<li><b>Testing Process</b>: Using Facade Method makes the process of testing
	comparatively easy since it has convenient methods for common testing tasks.
	</li>
	<li><b>Loose Coupling</b>: Availability of loose coupling between the
	clients and the Subsystems.</li>
	</ul>
	"""
#protectedstart classComments#######################################################################
#protectedend ######################################################################################



#	default constructor  def __init__(self):
#protectedstart classVars ##########################################################################
#protectedend ######################################################################################


	def __init__(self):
#protectedstart classVars ##########################################################################
#protectedend ######################################################################################

		self.start_component = ComponentManagementGeneralController()
		self.stop_component = ComponentManagementGeneralController()
		self.restart_component = ComponentManagementGeneralController()
		self.component_discovery = ComponentManagementGeneralController()
		self.register_component = ComponentManagementGeneralController()
		self.list_components = ComponentManagementGeneralController()
		self.get_component_info = ComponentManagementGeneralController()
		self.update_component = ComponentManagementGeneralController()

#protectedstart functions ##########################################################################
#protectedend ######################################################################################


