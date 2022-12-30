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
		self.web_map__search_cot = UtilGeneralController()
		self.protobuf_to_domain_parsing = UtilGeneralController()
		self.json_to_domain_parsing = UtilGeneralController()
		self.presense__update = UtilGeneralController()
		self.web_map__measure_distances = UtilGeneralController()
		self.presence__connect = UtilGeneralController()
		self.data_package__generate_show_qr_code = UtilGeneralController()
		self.send_welcome_message = UtilGeneralController()
		self.rest_api_push_kml = UtilGeneralController()
		self.presence__delete = UtilGeneralController()
		self.asci_welcome = UtilGeneralController()
	

