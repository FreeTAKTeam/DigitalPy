import inspect
from typing import Any
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.factory import Factory
import json
import importlib


class DefaultFactory(Factory):
    required_interfaces = {
        "event_manager": "digitalpy.core.main.event_manager.EventManager",
        "logger": "logger.Logger",
        "log_manager": "log_manager.LogManager",
        "session": "session.Session",
        "configuration": "digitalpy.core.configuration.Configuration",
        "message": "message.Message",
        "persistence_facade": "wcmf\lib\persistence\PersistenceFacade",
        "concurrency_manager": "concurrency_manager.ConcurrencyManager",
        "action_mapper": "digitalpy.core.zmanager.action_mapper.ActionMapper",
        "request": "digitalpy.core.zmanager.request.Request",
        "response": "digitalpy.core.zmanager.response.Response",
        "list_strategies": "list_strategy.ListStrategy",
        "formats": "digitalpy.core.parsing.format.Format",
        "formatter": "digitalpy.core.parsing.formatter.Formatter",
        "principal_factory": "principal_factory.PrincipalFactory",
    }

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.current_stack = []
        # factory instance is registered for use by the routing worker so that
        # the instances in the instance dictionary can be preserved when the
        # new object factory is instantiated in the sub-process
        self.instances = {
            'configuration': self.configuration,
            'factory': self,
        }
        # store imported modules to prevent multiple imports
        self.modules = {}

    def add_interfaces(self, interfaces: dict):
        raise NotImplementedError("this method has not yet been implemented")

    def clear(self):
        self.current_stack = []
        self.instances = {
            'configuration': self.configuration,
            'factory': self,
        }
        self.modules = {}
        DefaultFactory.required_interfaces = {
            "event_manager": "digitalpy.core.main.event_manager.EventManager",
            "logger": "logger.Logger",
            "log_manager": "log_manager.LogManager",
            "session": "session.Session",
            "configuration": "digitalpy.core.configuration.Configuration",
            "message": "message.Message",
            "persistence_facade": "wcmf\lib\persistence\PersistenceFacade",
            "concurrency_manager": "concurrency_manager.ConcurrencyManager",
            "action_mapper": "digitalpy.core.zmanager.action_mapper.ActionMapper",
            "request": "digitalpy.core.zmanager.request.Request",
            "response": "digitalpy.core.zmanager.response.Response",
            "list_strategies": "list_strategy.ListStrategy",
            "formats": "digitalpy.core.parsing.format.Format",
            "formatter": "digitalpy.core.parsing.formatter.Formatter",
            "principal_factory": "principal_factory.PrincipalFactory",
        }

    def get_instance(self, name, dynamic_configuration={}) -> object:
        instance = None
        self.current_stack.append(name)
        instance_key = self.get_instance_key(name, dynamic_configuration)
        if instance_key in self.instances and dynamic_configuration.get("__cached", True) is True:
            instance = self.instances[instance_key]
        else:
            static_configuration = self.configuration.get_section(name, True)
            configuration = dict(static_configuration, **dynamic_configuration)
            instance = self.create_instance(name, configuration, instance_key)
        self.current_stack.pop()
        return instance

    def get_instance_key(self, name, dynamic_configuration: dict):
        """Get the instance key for the given name and dynamic configuration"""
        key_conf = dynamic_configuration.copy()

        # remove the __cached key from the configuration
        key_conf.pop("__cached", None)
        
        if len(key_conf) == 0:
            instance_key = name.lower()
        else:
            try:
                instance_key = name + json.dumps(key_conf, sort_keys=True)
            # exception caught where the values of dynamic_configuration are not json serializable
            # but are required to be passed as arguments
            except TypeError:
                instance_key = name

        return instance_key

    def create_instance(self, name, configuration, instance_key):
        instance = None
        if configuration.get("__class") is not None:
            class_name = configuration.get("__class")
            class_name_parts = class_name.split(".")
            if len(class_name_parts) == 2:
                instance_class = getattr(
                    self.import_module(class_name_parts[0]),
                    class_name_parts[1],
                )
            else:
                instance_class = getattr(
                    self.import_module(".".join(class_name_parts[:-1])),
                    class_name_parts[-1],
                )

            if callable(getattr(instance_class, "__init__", None)):
                c_params = {}
                instance_class_func = getattr(instance_class, "__init__")
                instance_class_params = inspect.signature(instance_class_func)
                for (
                    param_name,
                    param_default,
                ) in instance_class_params.parameters.items():
                    if (
                        param_name == "self"
                        or param_name == "args"
                        or param_name == "kwargs"
                    ):
                        continue
                    param_instance_key = param_name.lower().replace("_", "")
                    # first check the configuration section for the parameter
                    if param_name in configuration:
                        c_params[param_name] = self.resolve_value(
                            configuration[param_name]
                        )
                    # then check if a parameter has already been initialized
                    elif param_instance_key in self.instances:
                        c_params[param_name] = self.instances[param_instance_key]
                    # check if a section with the name of the parameter exists
                    elif self.configuration.has_section(param_name):
                        c_params[param_name] = self.get_instance(param_name)
                    # check if a section with the name of the parameter in lowercase exists
                    elif self.configuration.has_section(param_instance_key):
                        c_params[param_name] = self.get_instance(
                            param_instance_key)
                    elif isinstance(param_default, inspect._empty):
                        raise Exception(
                            f"constructor parameter {param_name} in class {name} cannot be injected"
                        )
                instance = instance_class(**c_params)
                interface = self.get_interface(name)
                if interface != None and not isinstance(instance, interface):
                    raise Exception(
                        f"class {instance_class} is required to implement interface {interface}"
                    )

                if (
                    "__shared" not in configuration
                    or configuration["__shared"] == "true"
                ):
                    self.register_instance(instance_key, instance)

                for key, value in configuration.items():
                    if not key.startswith("__") and c_params.get(key, None) != None:
                        value = self.resolve_value(value)
                        setter_name = self.get_setter_name(key)
                        if getattr(instance, setter_name, None) != None:
                            getattr(instance, setter_name)(value)
                        else:
                            setattr(instance, key, value)
        else:
            # TODO: figure out the cases for a mapping being called and how to implement
            interface = self.get_interface(name)
            for key, value in configuration.items():
                if value[0] == "$":
                    obj = self.get_instance(value.strip("$"))
                    if interface is not None and not isinstance(obj, interface):
                        raise ValueError(
                            f"class of {name}.{key} is required to implement interface {interface}."
                        )
                    configuration[key] = obj
            self.register_instance(instance_key, configuration)
            instance = configuration
        return instance

    def get_setter_name(self, property):
        return "set" + property

    def resolve_value(self, value):
        if isinstance(value, str):
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            try:
                value = int(value)
            except ValueError:
                try:
                    value = self.get_instance(value)
                except ValueError:
                    pass
        if isinstance(value, list):
            result = []
            contains_instance = False

            for val in value:
                if (
                    isinstance(val, str)
                    and val.lower() != "true"
                    and val.lower() != "false"
                ):
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
            class_name_parts = class_name.split(".")
            if len(class_name_parts) == 2:
                instance_class = getattr(
                    importlib.import_module(".", class_name_parts[0]),
                    class_name_parts[1],
                )
            else:
                instance_class = getattr(
                    importlib.import_module(".".join(class_name_parts[:-1])),
                    class_name_parts[-1],
                )

            return instance_class
        return None

    def register_instance(self, name, instance):
        instance_key = name.lower()
        self.instances[instance_key] = instance

    def get_instance_of(self, class_name, dynamic_configuration={}):
        configuration = {
            **{"__class": class_name, "__shared": False},
            **dynamic_configuration,
        }
        # check if an instance of the class has already been created note this is only applicable
        # for classes that have a defined section in a configuration file
        if class_name in self.instances:
            instance = self.instances[class_name]
        else:
            instance = self.create_instance(class_name, configuration, None)
        return instance

    def get_new_instance(self, name, dynamic_configuration={}):
        configuration = {**dynamic_configuration, "__shared": False}
        instance = self.get_instance(name, configuration)
        return instance

    def clear_instance(self, name):
        instance_key = name.lower()
        if instance_key in self.instances:
            del self.instances[instance_key]

    def import_module(self, module_name):
        module = self.modules.get(module_name)
        if module is None:
            module = importlib.import_module(module_name)
            self.modules[module_name] = module
        return module

    def __getstate__(self) -> object:
        tmp_dict = self.__dict__.copy()
        if "modules" in tmp_dict:
            del tmp_dict["modules"]
        return tmp_dict

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.modules = {}
