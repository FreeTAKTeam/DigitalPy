from factory import Factory


class ObjectFactory:
    __factory = None

    @staticmethod
    def configure(factory: Factory):
        ObjectFactory.__factory = factory

    @staticmethod
    def get_instance(name, dynamicConfiguration={}):
        ObjectFactory.__check_config()
        return ObjectFactory.__factory.get_instance(name, dynamicConfiguration)

    @staticmethod
    def __check_config():
        if ObjectFactory.__factory is None:
            raise Exception("No Factory instance provided. Do this by calling the configure() method.")