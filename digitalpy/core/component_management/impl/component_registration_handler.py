import importlib
import os
from pathlib import PurePath
from typing import Dict, List
import pkg_resources

from digitalpy.core.main.registration_handler import RegistrationHandler
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.main.object_factory import ObjectFactory

MANIFEST = "manifest"
DIGITALPY = "digitalpy"
REQUIRED_ALFA_VERSION = "requiredAlfaVersion"
NAME = "name"
VERSION = "version"
ID = "UUID"
VERSION_DELIMITER = "."
DEPENDENCIES = "dependencies"

class ComponentRegistrationHandler(RegistrationHandler):
    """this class is used to manage component registration"""

    registered_components: Dict[str, DefaultFacade] = {}

    pending_components = {}

    component_index: Dict[str, Configuration] = {}

    @staticmethod
    def clear():
        ComponentRegistrationHandler.registered_components = {}
        ComponentRegistrationHandler.pending_components = {}

    @staticmethod
    def discover_components(component_folder_path: PurePath) -> List[str]:
        """this method is used to discover all available components

        Args:
            component_folder_path (str): the path in which to search for components. the searchable folder should be in the following format:\n
                component_folder_path \n
                |-- some_component \n
                |   `-- some_component_facade.py\n
                `-- another_component\n
                    `-- another_component_facade.py\n
        Returns:
            List[str]: a list of available components in the given path
        """
        potential_components = os.scandir(component_folder_path)
        components = []
        for potential_component in potential_components:
            facade_path = PurePath(
                potential_component.path, potential_component.name + "_facade.py"
            )
            if os.path.exists(facade_path):
                components.append(PurePath(potential_component.path))
        return components

    @staticmethod
    def register_component(
        component_path: PurePath, import_root: str, config: InifileConfiguration
    ) -> bool:
        """this method is used to register a given component

        Args:
            component_path (PurePath): the path to the directory of the component to be registered.
            import_root (str): the import root from which to import the components facade.
            config (InifileConfiguration): the main configuration through which the components actions should be exposed.

        Returns:
            bool: whether or not the component was registered successfully
        """
        try:
            facade_path = PurePath(component_path, component_path.name + "_facade.py")
            if os.path.exists(str(facade_path)):
                component_name = component_path.name.replace("_component", "")

                component_facade = getattr(
                    importlib.import_module(
                        f"{import_root}.{component_path.name}.{component_name}_facade"
                    ),
                    f"{''.join([name.capitalize() if name[0].isupper()==False else name for name in component_name.split('_')])}",
                )
                
                facade_instance: DefaultFacade = component_facade(
                    ObjectFactory.get_instance("SyncActionMapper"),
                    ObjectFactory.get_new_instance("request"),
                    ObjectFactory.get_new_instance("response"),
                    config
                )
                valid_manifest, pending = ComponentRegistrationHandler.validate_manifest(
                    facade_instance.get_manifest(), component_name, facade_instance
                )
                ComponentRegistrationHandler.save_component(facade_instance, component_name)
                if valid_manifest and not pending:
                    facade_instance.register(config)
                    ComponentRegistrationHandler.register_pending(component_name, config)
                    return True
                elif valid_manifest and pending:
                    return True
                else:
                    return False
            else:
                return False

            return True
        except Exception as e:
            # must use a print because logger may not be available
            print(f"failed to register component: {component_path}, with error: {e}")
            return False

    @staticmethod
    def save_component(facade: DefaultFacade, component_name: str):
        ComponentRegistrationHandler.registered_components[component_name] = facade
        ComponentRegistrationHandler.component_index[component_name] = facade.get_manifest()

    @staticmethod
    def register_pending(component_name, config):
        for facade_instance in ComponentRegistrationHandler.pending_components.pop(component_name, []):
            facade_instance.register(config)

    @staticmethod
    def validate_manifest(manifest: Configuration, component_name: str, component_facade) -> tuple[bool, bool]:
        #TODO: determine better way to inform the caller that the manifest is invalid
        """validate that the component is compatible with the current digitalpy version

        Args:
            manifest (Configuration): the manifest of a component to be validated for this digitalpy installation
            component_name (str): the name of the component to be validated

        Raises:
            ValueError: raised if the manifest section is missing from the manifest configuration

        Returns:
            tuple[bool, bool]: whether the component is compatible with the current digitalpy installation and whether the component has any pending dependencies
        """
        # retrieve the current digitalpy version based on the setup.py
        digitalpy_version = pkg_resources.require(DIGITALPY)[0].version

        try:
            # get the manifest section from the configuration
            section = manifest.get_section(component_name + MANIFEST, include_meta=True)
        except ValueError:

            raise ValueError(
                f"manifest section missing, requires name {component_name+MANIFEST} please add the \
                following section to the manifest [{component_name+MANIFEST}], for more information on component\
                manifests please refer to the digitalpy documentation"
            )

        # validate the component name matches the name specified in the manifest
        if component_name != section[NAME]:
            return False, False

        # iterate the delimited version number and compare it to the digitalpy version
        for i in range(len(section[REQUIRED_ALFA_VERSION].split(VERSION_DELIMITER))):
            #check if the version matches
            digitalpy_version_number = digitalpy_version.split(VERSION_DELIMITER)[i] if len(digitalpy_version.split(VERSION_DELIMITER))>i else 0
            if int(digitalpy_version_number)>int(section[REQUIRED_ALFA_VERSION].split(VERSION_DELIMITER)[i]):
                break
            elif int(digitalpy_version_number)==int(section[REQUIRED_ALFA_VERSION].split(VERSION_DELIMITER)[i]):
                continue
            else:
                return False, False
            
        # dont approve the manifest if the component has already been registered
        if (
            component_name in ComponentRegistrationHandler.registered_components
            and section[VERSION]
            != ComponentRegistrationHandler.registered_components[component_name][VERSION]
        ):
            return False, False

        # dont approve the manifest if a component with the same name but a different ID already exists
        if (
            component_name in ComponentRegistrationHandler.registered_components
            and ComponentRegistrationHandler.registered_components[component_name][ID]
            != section[ID]
        ):
            return False, False

        pending = False

        if (
            section.get(DEPENDENCIES, None) is not None 
            and section[DEPENDENCIES] != ""
        ):
            for dependency in section[DEPENDENCIES].split(","):
                if dependency not in ComponentRegistrationHandler.registered_components:
                    pending = True
                    if ComponentRegistrationHandler.pending_components.get(dependency) is not None:
                        ComponentRegistrationHandler.pending_components[dependency].append(component_facade)

                    else:
                        ComponentRegistrationHandler.pending_components[dependency] = [component_facade]

        return True, pending
