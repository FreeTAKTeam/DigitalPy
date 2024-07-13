from typing import TYPE_CHECKING, List, Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# import tables in initialization order
from digitalpy.core.component_management.persistence.component import Component as DBComponent
from digitalpy.core.component_management.persistence.error import Error as DBError

# import domain model classes
from digitalpy.core.component_management.domain.model.component import Component
from digitalpy.core.component_management.domain.model.error import Error

from digitalpy.core.main.controller import Controller
from digitalpy.core.component_management.persistence.component_management_base import Component_ManagementBase
from digitalpy.core.component_management.configuration.component_management_constants import DB_PATH

if TYPE_CHECKING:
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.action_mapper import ActionMapper


class Component_ManagementPersistenceController(Controller):
    """this class is responsible for handling the persistence of the Component_Management
    component. It is responsible for creating, removing and retrieving records.
    """

    def __init__(
        self,
        request: 'Request',
        response: 'Response',
        sync_action_mapper: 'ActionMapper',
        configuration: 'Configuration',
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.ses = self.create_db_session()

    def create_db_session(self) -> Session:
        """open a new session in the database

        Returns:
            Session: the session connecting the db
        """
        engine = create_engine(DB_PATH)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine)

        Component_ManagementBase.metadata.create_all(engine)

        # create a Session
        return SessionClass()

    # Begin methods for component table


    def save_component(self, component: Component, *args, **kwargs) -> 'DBComponent':
        if not isinstance(component, Component):
            raise TypeError("'Component' must be an instance of Component")

        db_component = DBComponent()
        db_component.oid = component.oid
        db_component.import_root = component.import_root
        db_component.installation_path = component.installation_path
        db_component.author = component.author
        db_component.author_email = component.author_email
        db_component.description = component.description
        db_component.License = component.License
        db_component.repo = component.repo
        db_component.requiredAlfaVersion = component.requiredAlfaVersion
        db_component.URL = component.URL
        db_component.Version = component.Version
        db_component.UUID = component.UUID
        self.ses.add(db_component)
        self.ses.commit()
        return db_component


    def remove_component(self, component: Component, *args, **kwargs):
        if not isinstance(component, Component):
            raise TypeError("'Component' must be an instance of Component")
        component_db = self.get_component(oid=component.oid)[0]
        self.ses.delete(component_db)
        self.ses.commit()

    def get_component(self, import_root:Union['str', None] = None, installation_path:Union['str', None] = None, author:Union['str', None] = None, author_email:Union['str', None] = None, description:Union['str', None] = None, License:Union['str', None] = None, repo:Union['str', None] = None, requiredAlfaVersion:Union['str', None] = None, URL:Union['str', None] = None, Version:Union['str', None] = None, UUID:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBComponent]:

        query = self.ses.query(DBComponent)

        if oid != None:
            query = query.filter(DBComponent.oid == oid)
        if import_root != None:
            query = query.filter(DBComponent.import_root == import_root)
        if installation_path != None:
            query = query.filter(DBComponent.installation_path == installation_path)
        if author != None:
            query = query.filter(DBComponent.author == author)
        if author_email != None:
            query = query.filter(DBComponent.author_email == author_email)
        if description != None:
            query = query.filter(DBComponent.description == description)
        if License != None:
            query = query.filter(DBComponent.License == License)
        if repo != None:
            query = query.filter(DBComponent.repo == repo)
        if requiredAlfaVersion != None:
            query = query.filter(DBComponent.requiredAlfaVersion == requiredAlfaVersion)
        if URL != None:
            query = query.filter(DBComponent.URL == URL)
        if Version != None:
            query = query.filter(DBComponent.Version == Version)
        if UUID != None:
            query = query.filter(DBComponent.UUID == UUID)

        return query.all()


    def get_all_component(self, *args, **kwargs) -> list[DBComponent]:
        return self.ses.query(DBComponent).all()

    def update_component(self, component: Component, *args, **kwargs):
        if not isinstance(component, Component):
            raise TypeError("'component' must be an instance of Component")
        component_db = self.get_component(oid = component.oid)[0]
        component_db.import_root = component.import_root
        component_db.installation_path = component.installation_path
        component_db.author = component.author
        component_db.author_email = component.author_email
        component_db.description = component.description
        component_db.License = component.License
        component_db.repo = component.repo
        component_db.requiredAlfaVersion = component.requiredAlfaVersion
        component_db.URL = component.URL
        component_db.Version = component.Version
        component_db.UUID = component.UUID
        self.ses.commit()

    # Begin methods for component table

    # Begin methods for error table


    def save_error(self, error: Error, *args, **kwargs) -> 'DBError':
        if not isinstance(error, Error):
            raise TypeError("'Error' must be an instance of Error")

        db_error = DBError()
        db_error.oid = error.oid
        self.ses.add(db_error)
        self.ses.commit()
        return db_error


    def remove_error(self, error: Error, *args, **kwargs):
        if not isinstance(error, Error):
            raise TypeError("'Error' must be an instance of Error")
        error_db = self.get_error(oid=error.oid)[0]
        self.ses.delete(error_db)
        self.ses.commit()

    def get_error(self, oid: 'str' = None, *args, **kwargs) -> List[DBError]:

        query = self.ses.query(DBError)

        if oid != None:
            query = query.filter(DBError.oid == oid)

        return query.all()


    def get_all_error(self, *args, **kwargs) -> list[DBError]:
        return self.ses.query(DBError).all()

    def update_error(self, error: Error, *args, **kwargs):
        if not isinstance(error, Error):
            raise TypeError("'error' must be an instance of Error")
        error_db = self.get_error(oid = error.oid)[0]
        self.ses.commit()

    # Begin methods for error table


    def __getstate__(self) -> object:
        state: dict = super().__getstate__()  # type: ignore
        if "ses" in state:
            del state["ses"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.ses = self.create_db_session()
