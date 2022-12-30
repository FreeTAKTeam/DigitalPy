from Catalog.Data.Domain.FTS_Model.Facade import Facade

class COTManagementFacade(Facade, Facade):
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
		self.build_drop_point_object = COTManagementGeneralController()
		self.cot__share_privately = COTManagementGeneralController()
		self.cot_record_in_db = COTManagementGeneralController()
		self.cot__broadcast = COTManagementGeneralController()
		self.medevac__receive = COTManagementGeneralController()
		self.web_ui_manage_presence = COTManagementGeneralController()
		self.medevac__send = COTManagementGeneralController()
	

