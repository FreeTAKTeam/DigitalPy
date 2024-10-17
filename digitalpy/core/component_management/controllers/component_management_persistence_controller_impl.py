from typing import TYPE_CHECKING

# import tables in initialization order

# import domain model classes
from digitalpy.core.component_management.domain.model.component import Component



from digitalpy.core.component_management.controllers.component_management_persistence_controller import (
    Component_managementPersistenceController,
)


if TYPE_CHECKING:
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
    from digitalpy.core.zmanager.action_mapper import ActionMapper


class Component_managementPersistenceControllerImpl(Component_managementPersistenceController):
    """this class is responsible for handling the persistence of the component_management
    component. It is responsible for creating, removing and retrieving records.
    """

    def __init__(
        self,
        request: "Request",
        response: "Response",
        sync_action_mapper: "ActionMapper",
        configuration: "Configuration",
    ):
        super().__init__(request, response, sync_action_mapper, configuration)

    def update_component(self, component: Component, *args, **kwargs):
        if not isinstance(component, Component):
            raise TypeError("'component' must be an instance of Component")
        with self.ses.begin() as session:
            component_db = self.get_component(UUID=component.UUID)[0]
            component_db.author = component.author
            component_db.author_email = component.author_email
            component_db.description = component.description
            component_db.License = component.License
            component_db.repo = component.repo
            component_db.requiredAlfaVersion = component.requiredAlfaVersion
            component_db.URL = component.URL
            component_db.Version = component.Version
            component_db.UUID = component.UUID
            component_db.isActive = component.isActive
            component_db.isInstalled = component.isInstalled
            component_db.installationPath = component.installationPath
            component_db.name = component.name
            session.commit()

    # Begin methods for error table

    def __getstate__(self) -> object:
        state: dict = super().__getstate__()  # type: ignore
        if "ses" in state:
            del state["ses"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.ses = self.create_db_session()
