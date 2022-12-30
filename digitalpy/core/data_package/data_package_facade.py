from Catalog.Data.Domain.FTS_Model.Facade import Facade

class DataPackageFacade(Facade, Facade):
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
		self.data_package__download_file_https = DataPackageGeneralController()
		self.data_package__upload_file_https = DataPackageGeneralController()
		self.data_package__download_file_http = DataPackageGeneralController()
		self.replay_hystory = DataPackageGeneralController()
		self.data_package___file_list_http = DataPackageGeneralController()
		self.data_package__generate_show_qr_code = DataPackageGeneralController()
		self.data_package__upload_file = DataPackageGeneralController()
		self.data_package__delete_file = DataPackageGeneralController()
		self.data_package__download_file = DataPackageGeneralController()
		self.data_package__is_private = DataPackageGeneralController()
		self.data_package__upload_file_http = DataPackageGeneralController()
		self.data_package__file_list = DataPackageGeneralController()
		self.broadcast_data_package_to_all_users = DataPackageGeneralController()
		self.excheck__join_existing_checklist = DataPackageGeneralController()
		self.enrollment = DataPackageGeneralController()
		self.data_package__file_list_https = DataPackageGeneralController()
	

