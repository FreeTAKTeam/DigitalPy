import inspect
from configuration import Configuration
from factory import Factory
import json
import importlib

class DefaultFactory(Factory):
    required_interfaces = {
        'eventManager' :          'event_manager.EventManager',
        'logger' :                'logger.Logger',
        'logManager' :            'log_manager.LogManager',
        'session' :               'session.Session',
        'configuration' :         'configuration.Configuration',
        'message' :               'message.Message',
        'persistenceFacade' :     'wcmf\lib\persistence\PersistenceFacade',
        'concurrencyManager' :    'concurrency_manager.ConcurrencyManager',
        'actionMapper' :          'action_mapper.ActionMapper',
        'request' :               'request.Request',
        'response' :              'response.Response',
        'listStrategies' :        'list_strategy.ListStrategy',
        'formats' :               'format.Format',
        'formatter' :             'formatter.Formatter',
        'principalFactory' :      'principal_factory.PrincipalFactory',
    }

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.current_stack = []
        self.instances = []

    def get_instance(self, name, dynamic_configuration={}) -> object:
        instance = None
        self.current_stack.append(name)
        if len(dynamic_configuration) == 0:
            instance_key = name.lower()
        else:
            instance_key = name + json.dumps(dynamic_configuration)
        if instance_key in self.instances:
            instance = self.instances[instance_key]
        else:
            static_configuration = self.configuration.get_section(name, True)
            configuration = dict(static_configuration, **dynamic_configuration)
            instance = self.create_instance(name, configuration, instance_key)
        self.current_stack.pop()
        return instance

    def create_instance(self, name, configuration, instance_key):
        instance = None

        c_params = {}
        instance_class = importlib.import_module(name)
        if callable(getattr(instance_class, "__init__", None)):
            instance_class_func = getattr(instance_class, "__init__")
            instance_class_params = inspect.getargvalues(instance_class_func)
            for param_name, param_default in instance_class_params:
                param_instance_key = param_name.lower()
                if param_instance_key in self.instances:
                    c_params[param_name] = self.instances[param_instance_key]
                elif param_name in configuration:
                    c_params[param_name] = self.resolve_value(configuration[param_name])
                elif self.configuration.has_section(param_name):
                    c_params[param_name] = self.get_instance(param_name)
                elif param_default == None:
                    raise Exception(f"constructor parameter {param_name} in class {name} cannot be injected")
                del configuration[param_name]
            instance = instance_class(**c_params)
            interface = self.get_interface()
            if interface != None and not isinstance(instance, interface):
                raise Exception(f'class {instance_class} is required to implement interface {interface}')
            for key, val in configuration.items():
                if not key.startswith("__") and c_params.get(key, None) != None:
                    value = self.resolve_value(value)
                    setter_name = self.get_setter_name(key)
                    if getattr(instance, setter_name, None) != None:
                        getattr(instance, setter_name)(value)
                    else:
                        setattr(instance, key, value)
        else:
            #TODO: figure out the cases for a mapping being called and how to implement
            raise NotImplementedError
        return instance

    def get_setter_name(self, property):
        return 'set'+property
    
    def resolve_value(self, value):
        if isinstance(value, str):
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            else:
                value = self.get_instance(value)

        if isinstance(value, list):
            result = []
            contains_instance = False

            for val in value:
                if isinstance(val, str) and val.lower() != 'true' and val.lower() != 'false':
                    result.append(self.get_instance(val))
                    contains_instance = True
                else:
                    result.append(val)
            if contains_instance:
                value = result
        return value
    
    def get_interface(self, name):
        if name in DefaultFactory.required_interfaces:
            return DefaultFactory.required_interfaces[name]
        return None

    def register_instance(self, name, instance):
        instance_key = name.lower()
        self.instances[instance_key] = instance

    def get_new_instance(self, name, dynamic_configuration={}):
        instance = self.get_instance(name, dynamic_configuration)
        return instance