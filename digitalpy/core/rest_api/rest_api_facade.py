from Catalog.Data.Domain.FTS_Model.Facade import Facade

class RESTAPIFacade(Facade, Facade):
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
		self.web_ui_manage_presence = RESTAPIGeneralController()
		self.api_sensorpostspi = RESTAPIGeneralController()
		self.api_sensor = RESTAPIGeneralController()
		self.api_exchecktable = RESTAPIGeneralController()
		self.api_excheck_table = RESTAPIGeneralController()
		self.api_managechat = RESTAPIGeneralController()
		self.api_apiuser = RESTAPIGeneralController()
		self.api_missiontable = RESTAPIGeneralController()
		self.fth__telegram_integration = RESTAPIGeneralController()
		self.api_systemuserpostsystemuser = RESTAPIGeneralController()
		self.api_managegeoobjectgetgeoobject = RESTAPIGeneralController()
		self.api_managegeoobject = RESTAPIGeneralController()
		self.api_events = RESTAPIGeneralController()
		self.api_system_health = RESTAPIGeneralController()
		self.web_ui__send_message = RESTAPIGeneralController()
		self.api_generateqr = RESTAPIGeneralController()
		self.fth__telegram_integration__datapackage = RESTAPIGeneralController()
		self.api_managegeoobjectputgeoobject = RESTAPIGeneralController()
		self.api_mapvid = RESTAPIGeneralController()
		self.api_authenticateuser = RESTAPIGeneralController()
		self.api_managekmlpostkml = RESTAPIGeneralController()
		self.api_manageroutepostroute = RESTAPIGeneralController()
		self.api_manageroute = RESTAPIGeneralController()
		self.fth__video_server = RESTAPIGeneralController()
		self.api_clients = RESTAPIGeneralController()
		self.api_manageemergencygetemergency = RESTAPIGeneralController()
		self.api_managepresenceputpresence = RESTAPIGeneralController()
		self.api_managesystemuserputsystemuser = RESTAPIGeneralController()
		self.web_ui__send_cot = RESTAPIGeneralController()
		self.api_sendgeochat = RESTAPIGeneralController()
		self.api_sensorpostdrone = RESTAPIGeneralController()
		self.api_managechatpostchattoall = RESTAPIGeneralController()
		self.api_managevideostream = RESTAPIGeneralController()
		self.api_managenotificationgetnotification = RESTAPIGeneralController()
		self.api_url = RESTAPIGeneralController()
		self.api_managevideostreampostvideostream = RESTAPIGeneralController()
		self.api_manageemergencypostemergency = RESTAPIGeneralController()
		self.api_addsystemuser = RESTAPIGeneralController()
		self.api_datapackagetable = RESTAPIGeneralController()
		self.api_managegeoobjectpostgeoobject = RESTAPIGeneralController()
		self.api_managecotgetzonecot = RESTAPIGeneralController()
		self.api_managevideostreamgetvideostream = RESTAPIGeneralController()
		self.fth__kml_forms = RESTAPIGeneralController()
		self.api_manageemergency = RESTAPIGeneralController()
		self.fth__telegram_integration__chat_to_all = RESTAPIGeneralController()
		self.api_recentcot = RESTAPIGeneralController()
		self.api_broadcastdatapackage = RESTAPIGeneralController()
		self.api_systemuserdeletesystemuser = RESTAPIGeneralController()
		self._api_logs = RESTAPIGeneralController()
		self.api_managepresencepostpresence = RESTAPIGeneralController()
		self.api_serviceinfo = RESTAPIGeneralController()
		self.api_manageemergencydeleteemergency = RESTAPIGeneralController()
		self.api_managepresence = RESTAPIGeneralController()
		self.api_federationtable = RESTAPIGeneralController()
		self.api_alive = RESTAPIGeneralController()
		self.api_managevideostreamdeletevideostream = RESTAPIGeneralController()
		self.api_manageapigethelp = RESTAPIGeneralController()
	

