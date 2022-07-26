from default_factory import DefaultFactory
from inifile_configuration import InifileConfiguration
from object_factory import ObjectFactory

def test_basic_configuration():
    config = InifileConfiguration(".")
    config.add_configuration("test_router.ini")
    
    ObjectFactory.configure(DefaultFactory(config))
    ObjectFactory.register_instance('configuration', config)

    request = ObjectFactory.get_new_instance('request')
    request.set_action("Emergency")

    actionmapper = ObjectFactory.get_instance('actionMapper')
    response = ObjectFactory.get_new_instance('response')
    actionmapper.process_action(request, response)
    return response