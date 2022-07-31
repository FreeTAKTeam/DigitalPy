from core.factory import Factory


class ObjectFactory:
    __factory = None

    @staticmethod
    def configure(factory: Factory):
        ObjectFactory.__factory = factory

    @staticmethod
    def get_instance(name, dynamic_configuration={}):
        ObjectFactory.__check_config()
        return ObjectFactory.__factory.get_instance(name, dynamic_configuration)

    @staticmethod
    def get_new_instance(name, dynamic_configuration={}):
        ObjectFactory.__check_config()
        return ObjectFactory.__factory.get_new_instance(name, dynamic_configuration)

    @staticmethod
    def __check_config():
        if ObjectFactory.__factory is None:
            raise Exception("No Factory instance provided. Do this by calling the configure() method.")

    @staticmethod
    def get_instance_of(class_name, dynamic_configuration={}):
        ObjectFactory.__check_config()
        return ObjectFactory.__factory.get_instance_of(class_name, dynamic_configuration)
    
    @staticmethod
    def register_instance(name, instance):
        ObjectFactory.__check_config()
        ObjectFactory.__factory.register_instance(name, instance)