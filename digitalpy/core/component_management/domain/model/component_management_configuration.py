# pylint: disable=invalid-name

from pathlib import Path
from typing import Union
from digitalpy.core.domain.node import Node

# iterating associations

class ComponentManagementConfiguration(Node):
    def __init__(self, model_configuration, model, oid=None, node_type="Component") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._component_installation_path: 'str' = None
        self._component_blueprint_path: 'str' = None
        self._component_import_root: 'str' = None

    @property
    def component_installation_path(self) -> 'str':
        """The path where components are installed."""
        return self._component_installation_path
    
    @component_installation_path.setter
    def component_installation_path(self, component_installation_path: Union['str', 'Path']):
        if isinstance(component_installation_path, Path):
            component_installation_path = str(component_installation_path)

        if not isinstance(component_installation_path, str):
            raise TypeError("'component_installation_path' must be of type str or Path")
        self._component_installation_path = component_installation_path

    @property
    def component_blueprint_path(self) -> 'str':
        """The path where component blueprints are stored."""
        return self._component_blueprint_path
    
    @component_blueprint_path.setter
    def component_blueprint_path(self, component_blueprint_path: 'str'):
        component_blueprint_path = str(component_blueprint_path)
        if not isinstance(component_blueprint_path, str):
            raise TypeError("'component_blueprint_path' must be of type str")
        self._component_blueprint_path = component_blueprint_path

    @property
    def component_import_root(self) -> 'str':
        """The path where components are imported."""
        return self._component_import_root
    
    @component_import_root.setter
    def component_import_root(self, component_import_root: 'str'):
        component_import_root = str(component_import_root)
        if not isinstance(component_import_root, str):
            raise TypeError("'component_import_root' must be of type str")
        self._component_import_root = component_import_root