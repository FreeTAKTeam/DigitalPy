from core.impl.default_factory import DefaultFactory
from config.impl.inifile_configuration import InifileConfiguration
from core.object_factory import ObjectFactory

def test_basic_configuration():
    config = InifileConfiguration("")
    config.add_configuration(r"C:\Users\natha\Documents\programmer_stuff\GIT\DigitalPy\tests\test_configuration\test_router.ini")
    
    ObjectFactory.configure(DefaultFactory(config))
    ObjectFactory.register_instance('configuration', config)

    request = ObjectFactory.get_new_instance('request')
    request.set_action("SendEmergency")
    
    actionmapper = ObjectFactory.get_instance('actionMapper')
    response = ObjectFactory.get_new_instance('response')
    actionmapper.process_action(request, response)
    return response