from Catalog.Data.Domain.FTS_Model.Facade import Facade

class HealthFacade(Facade, Facade):
    """Facade class for the this component. Responsible for handling all public
    routing. Forwards all requests to the internal router.
      WHY
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
	
# default constructor  def __init__(self):  

    def __init__(self):
		self.check_system_services = HealthGeneralController()
		self.monitor_system_performance = HealthGeneralController()
		self.check_network_connectivity = HealthGeneralController()
		self.check_system_updates = HealthGeneralController()
		self.health_check = HealthGeneralController()
		self.dashboard__system_health = HealthGeneralController()
		self.check_system_backups = HealthGeneralController()
		self.check_disk_space = HealthGeneralController()
		self.check_system_logs = HealthGeneralController()
		self.check_component_status = HealthGeneralController()
		self.check_system_security = HealthGeneralController()
	

