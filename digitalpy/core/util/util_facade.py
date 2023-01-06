from Catalog.Data.Domain.FTS_Model.Facade import Facade

class UtilFacade(Facade, Facade):
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
		self.about = UtilGeneralController()
		self.web_map_search_cot = UtilGeneralController()
		self.protobuf_to_domain_parsing = UtilGeneralController()
		self.json_to_domain_parsing = UtilGeneralController()
		self.presense_update = UtilGeneralController()
		self.web_map_measure_distances = UtilGeneralController()
		self.presence_connect = UtilGeneralController()
		self.data_package_generate_show_qr_code = UtilGeneralController()
		self.send_welcome_message = UtilGeneralController()
		self.rest_api_push_kml = UtilGeneralController()
		self.presence_delete = UtilGeneralController()
		self.asci_welcome = UtilGeneralController()
	

