from digitalpy.component.impl.default_facade import DefaultFacade
#protectedstart imports ############################################################################
#protectedend ######################################################################################


#protectedstart classDeclaration ###################################################################
class IAMFacade(DefaultFacade):
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

		self.delete_other_profiles = IAMGeneralController()
		self.view_profile = IAMGeneralController()
		self.assign_cot_to_group = IAMGeneralController()
		self.user_select = IAMGeneralController()
		self.excheck_delete_checklist_from_server = IAMGeneralController()
		self.users_create_user_with_mobile_cert = IAMGeneralController()
		self.delete_system_users = IAMGeneralController()
		self.iammanifest = IAMGeneralController()
		self.iam_adding,_updating,_and_reading_data = IAMGeneralController()
		self.create_reports = IAMGeneralController()
		self.logout = IAMGeneralController()
		self.delete_kml = IAMGeneralController()
		self.edit_profile = IAMGeneralController()
		self.excheck_start_new_checklist_from_a_template = IAMGeneralController()
		self.ssl_data_package = IAMGeneralController()
		self.login = IAMGeneralController()
		self.excheck_get_a_list_of_active_checklists = IAMGeneralController()
		self.directory_structure = IAMGeneralController()
		self.excheck_join_existing_checklist = IAMGeneralController()
		self.users_push_certs_to_connected_user = IAMGeneralController()
		self.iam_authentication = IAMGeneralController()
		self.excheck_delete_template_from_ui = IAMGeneralController()
		self.ssl_encryption = IAMGeneralController()
		self.users_create_user_with_no_cert = IAMGeneralController()
		self.iam_search = IAMGeneralController()
		self.delete_video_streams = IAMGeneralController()
		self.user_management = IAMGeneralController()
		self.excheck_get_a_list_of_existing_templates = IAMGeneralController()
		self.users_create_user_with_wintak_cert = IAMGeneralController()
		self.user_delete = IAMGeneralController()
		self.ssl_deactivate_certs = IAMGeneralController()
		self.create_emergency = IAMGeneralController()
		self.create_video_streams = IAMGeneralController()
		self.create_kml = IAMGeneralController()
		self.user_rest_api_key = IAMGeneralController()
		self.user_remove = IAMGeneralController()
		self.delete_reports = IAMGeneralController()

#protectedstart functions ##########################################################################
#protectedend ######################################################################################


