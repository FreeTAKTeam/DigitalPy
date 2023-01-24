from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper

class ServiceManagementActionMapper(DefaultActionMapper):
    """This is the Core ServiceManagement action mapper.  Each core Package must have its own action
    mapper to be loaded with the internal action mapping configuration and to be
    used by the facade for internal routing.
    """
