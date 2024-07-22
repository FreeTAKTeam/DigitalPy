from typing import Union
import uuid
from digitalpy.core.component_management.domain.builder.component_builder import ComponentBuilder
from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.domain.builder import Builder
from digitalpy.core.serialization.configuration.serialization_constants import Protocols
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.main.object_factory import ObjectFactory

from digitalpy.core.component_management.configuration.component_management_constants import COMPONENT

# import domain model classes
from digitalpy.core.component_management.domain.model.component import Component

from digitalpy.core.component_management.persistence.component import Component as DBComponent

class ComponentBuilderImpl(ComponentBuilder):
    """Builds a Component object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Component = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a Component object"""
        self.request.set_value("object_class_name", "Component")

        configuration = config_loader.find_configuration(COMPONENT)

        self.result = super()._create_model_object(
          configuration, extended_domain={"Component": Component,
                                        })

        # self.result = Component(model_configuration=None, model=None, oid=ObjectFactory.get_instance("ObjectID", {"id": str(uuid.uuid1()), "type": "Component"}), node_type="Component")

    def add_object_data(self, mapped_object: Union[bytes, str, DBComponent, dict], protocol=None):
        """adds the data from the mapped object to the Health object """
        super().add_object_data(mapped_object, protocol)
        # handle the case where the mapped object is a manifest
        if isinstance(mapped_object, dict):
            self._add_manifest_object_data(mapped_object)

    def _add_manifest_object_data(self, mapped_object: dict):
        """adds the data from the manifest object to the Component object
        
        Args:
            mapped_object (InifileConfiguration): the manifest object

        Returns:
            None
        """
        self.result.author = str(mapped_object.get("author"))
        self.result.author_email = str(mapped_object.get("author_email"))
        self.result.description = str(mapped_object.get("description"))
        self.result.License = str(mapped_object.get("License"))
        self.result.repo = str(mapped_object.get("repo"))
        self.result.requiredAlfaVersion = str(mapped_object.get("requiredAlfaVersion"))
        self.result.URL = str(mapped_object.get("URL"))
        self.result.Version = str(mapped_object.get("Version"))
        self.result.UUID = str(mapped_object.get("UUID"))
        self.result.name = str(mapped_object.get("name"))
        self.result.installationPath = str(mapped_object.get("installationPath"))
        self.result.isActive = bool(mapped_object.get("isActive"))
        self.result.isInstalled = bool(mapped_object.get("isInstalled"))
        self.result.name = str(mapped_object.get("name"))
