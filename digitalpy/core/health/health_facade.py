from digitalpy.component.impl.default_facade import DefaultFacade
#protectedstart imports ############################################################################
#protectedend ######################################################################################


#protectedstart classDeclaration ###################################################################
class HealthFacade(DefaultFacade):
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

		self.check_system_services = HealthGeneralController()
		self.monitor_system_performance = HealthGeneralController()
		self.check_network_connectivity = HealthGeneralController()
		self.check_system_updates = HealthGeneralController()
		self.health_check = HealthGeneralController()
		self.dashboard_system_health = HealthGeneralController()
		self.check_system_backups = HealthGeneralController()
		self.check_disk_space = HealthGeneralController()
		self.check_system_logs = HealthGeneralController()
		self.check_component_status = HealthGeneralController()
		self.check_system_security = HealthGeneralController()

#protectedstart functions ##########################################################################
#protectedend ######################################################################################


