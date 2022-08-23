import inspect
from digitalpy.config.configuration import Configuration
from digitalpy.core.factory import Factory
import json
import importlib

class DefaultFactory(Factory):
    required_interfaces = {
        'event_manager' :          'digitalpy.core.event_manager.EventManager',
        'logger' :                'logger.Logger',
        'log_manager' :            'log_manager.LogManager',
        'session' :               'session.Session',
        'configuration' :         'configuration.Configuration',
        'message' :               'message.Message',
        'persistence_facade' :     'wcmf\lib\persistence\PersistenceFacade',
        'concurrency_manager' :    'concurrency_manager.ConcurrencyManager',
        'action_mapper' :          'digitalpy.routing.action_mapper.ActionMapper',
        'request' :               'digitalpy.routing.request.Request',
        'response' :              'digitalpy.routing.response.Response',
        'list_strategies' :        'list_strategy.ListStrategy',
        'formats' :               'format.Format',
        'formatter' :             'formatter.Formatter',
        'principal_factory' :      'principal_factory.PrincipalFactory',
    }

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.current_stack = []
        self.instances = {}

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
        if configuration.get('__class') is not None:
            class_name = configuration.get('__class')
            class_name_parts = class_name.split('.')
            if len(class_name_parts)==2:
                instance_class = getattr(importlib.import_module('.',class_name_parts[0]), class_name_parts[1])
            else:
                instance_class = getattr(importlib.import_module(".".join(class_name_parts[:-1])), class_name_parts[-1])

            if callable(getattr(instance_class, "__init__", None)):
                c_params = {}
                instance_class_func = getattr(instance_class, "__init__")
                instance_class_params = inspect.signature(instance_class_func)
                for param_name, param_default in instance_class_params.parameters.items():
                    if param_name == "self" or param_name == 'args' or param_name == 'kwargs':
                        continue
                    param_instance_key = param_name.lower()
                    if param_instance_key in self.instances:
                        c_params[param_name] = self.instances[param_instance_key]
                    elif param_name in configuration:
                        c_params[param_name] = self.resolve_value(configuration[param_name])
                    elif self.configuration.has_section(param_name):
                        c_params[param_name] = self.get_instance(param_name)
                    elif param_default == None:
                        raise Exception(f"constructor parameter {param_name} in class {name} cannot be injected")
                instance = instance_class(**c_params)
                interface = self.get_interface(name)
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
            class_name = DefaultFactory.required_interfaces[name]
            class_name_parts = class_name.split('.')
            if len(class_name_parts)==2:
                instance_class = getattr(importlib.import_module('.',class_name_parts[0]), class_name_parts[1])
            else:
                instance_class = getattr(importlib.import_module(".".join(class_name_parts[:-1])), class_name_parts[-1])

            return instance_class
        return None

    def register_instance(self, name, instance):
        instance_key = name.lower()
        self.instances[instance_key] = instance

    def get_instance_of(self, class_name, dynamic_configuration={}):
        configuration = {**{'__class': class_name, '__shared': False}, **dynamic_configuration}
        instance = self.create_instance(class_name, configuration,None)
        return instance
        
    def get_new_instance(self, name, dynamic_configuration={}):
        instance = self.get_instance(name, dynamic_configuration)
        return instance