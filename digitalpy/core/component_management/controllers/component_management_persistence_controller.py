from typing import TYPE_CHECKING, List, Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

# import tables in initialization order
from digitalpy.core.component_management.persistence.component import (
    Component as DBComponent,
)
from digitalpy.core.component_management.persistence.actionkey import (
    ActionKey as DBActionKey,
)
from digitalpy.core.component_management.persistence.error import Error as DBError

# import domain model classes
from digitalpy.core.component_management.domain.model.component import Component
from digitalpy.core.component_management.domain.model.actionkey import ActionKey
from digitalpy.core.component_management.domain.model.error import Error

from digitalpy.core.main.controller import Controller
from digitalpy.core.component_management.persistence.component_management_base import (
    Component_managementBase,
)
from digitalpy.core.component_management.configuration.component_management_constants import (
    DB_PATH,
)

if TYPE_CHECKING:
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.action_mapper import ActionMapper


class Component_managementPersistenceController(Controller):
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
        self.ses = self.create_db_session()

    def create_db_session(self) -> Session:
        """open a new session in the database

        Returns:
            Session: the session connecting the db
        """
        # use NullPool to prevent connections from remaning open, this allows
        # us to delete the component and it's database at runtime (component management)
        engine = create_engine(DB_PATH, poolclass=NullPool)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine, expire_on_commit=False)

        Component_managementBase.metadata.create_all(engine)

        # create a Session
        return SessionClass

    # Begin methods for component table

    def save_component(self, component: Component, *args, **kwargs) -> "DBComponent":
        if not isinstance(component, Component):
            raise TypeError("'Component' must be an instance of Component")
        with self.ses.begin() as session:
            db_component = DBComponent()
            db_component.oid = component.oid
            db_component.author = component.author
            db_component.author_email = component.author_email
            db_component.description = component.description
            db_component.License = component.License
            db_component.repo = component.repo
            db_component.requiredAlfaVersion = component.requiredAlfaVersion
            db_component.URL = component.URL
            db_component.Version = component.Version
            db_component.UUID = component.UUID
            db_component.isActive = component.isActive
            db_component.isInstalled = component.isInstalled
            db_component.installationPath = component.installationPath
            db_component.name = component.name
            session.add(db_component)
            session.commit()
            return db_component

    def remove_component(self, component: Component, *args, **kwargs):
        if not isinstance(component, Component):
            raise TypeError("'Component' must be an instance of Component")
        with self.ses.begin() as session:
            component_db = self.get_component(oid=component.oid)[0]
            session.delete(component_db)
            session.commit()

    def get_component(
        self,
        author: Union["str", None] = None,
        author_email: Union["str", None] = None,
        description: Union["str", None] = None,
        License: Union["str", None] = None,
        repo: Union["str", None] = None,
        requiredAlfaVersion: Union["str", None] = None,
        URL: Union["str", None] = None,
        Version: Union["str", None] = None,
        UUID: Union["str", None] = None,
        isActive: Union["str", None] = None,
        isInstalled: Union["str", None] = None,
        installationPath: Union["str", None] = None,
        name: Union["str", None] = None,
        oid: "str" = None,
        *args,
        **kwargs
    ) -> List[DBComponent]:
        with self.ses.begin() as session:
            query = session.query(DBComponent)

            if oid != None:
                query = query.filter(DBComponent.oid == oid)
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
                query = query.filter(
                    DBComponent.requiredAlfaVersion == requiredAlfaVersion
                )
            if URL != None:
                query = query.filter(DBComponent.URL == URL)
            if Version != None:
                query = query.filter(DBComponent.Version == Version)
            if UUID != None:
                query = query.filter(DBComponent.UUID == UUID)
            if isActive != None:
                query = query.filter(DBComponent.isActive == isActive)
            if isInstalled != None:
                query = query.filter(DBComponent.isInstalled == isInstalled)
            if installationPath != None:
                query = query.filter(DBComponent.installationPath == installationPath)
            if name != None:
                query = query.filter(DBComponent.name == name)

            return query.all()

    def get_all_component(self, *args, **kwargs) -> list[DBComponent]:
        with self.ses.begin() as session:
            return session.query(DBComponent).all()

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

    # Begin methods for component table

    # Begin methods for actionkey table

    def save_actionkey(self, actionkey: ActionKey, *args, **kwargs) -> "DBActionKey":
        if not isinstance(actionkey, ActionKey):
            raise TypeError("'ActionKey' must be an instance of ActionKey")
        with self.ses.begin() as session:
            db_actionkey = DBActionKey()
            db_actionkey.oid = actionkey.oid
            db_actionkey.action = actionkey.action
            db_actionkey.context = actionkey.context
            db_actionkey.decorator = actionkey.decorator
            db_actionkey.config = actionkey.config
            db_actionkey.target = actionkey.target
            db_actionkey.source = actionkey.source
            db_actionkey.referencedBehaviour = actionkey.referencedBehaviour
            db_actionkey.name = actionkey.name
            session.add(db_actionkey)
            session.commit()
            return db_actionkey

    def remove_actionkey(self, actionkey: ActionKey, *args, **kwargs):
        if not isinstance(actionkey, ActionKey):
            raise TypeError("'ActionKey' must be an instance of ActionKey")
        with self.ses.begin() as session:
            actionkey_db = self.get_actionkey(oid=actionkey.oid)[0]
            session.delete(actionkey_db)
            session.commit()

    def get_actionkey(
        self,
        action: Union["str", None] = None,
        context: Union["str", None] = None,
        decorator: Union["str", None] = None,
        config: Union["str", None] = None,
        target: Union["str", None] = None,
        source: Union["str", None] = None,
        referencedBehaviour: Union["str", None] = None,
        name: Union["str", None] = None,
        oid: "str" = None,
        *args,
        **kwargs
    ) -> List[DBActionKey]:
        with self.ses.begin() as session:
            query = session.query(DBActionKey)

            if oid != None:
                query = query.filter(DBActionKey.oid == oid)
            if action != None:
                query = query.filter(DBActionKey.action == action)
            if context != None:
                query = query.filter(DBActionKey.context == context)
            if decorator != None:
                query = query.filter(DBActionKey.decorator == decorator)
            if config != None:
                query = query.filter(DBActionKey.config == config)
            if target != None:
                query = query.filter(DBActionKey.target == target)
            if source != None:
                query = query.filter(DBActionKey.source == source)
            if referencedBehaviour != None:
                query = query.filter(
                    DBActionKey.referencedBehaviour == referencedBehaviour
                )
            if name != None:
                query = query.filter(DBActionKey.name == name)

            return query.all()

    def get_all_actionkey(self, *args, **kwargs) -> list[DBActionKey]:
        with self.ses.begin() as session:
            return session.query(DBActionKey).all()

    def update_actionkey(self, actionkey: ActionKey, *args, **kwargs):
        if not isinstance(actionkey, ActionKey):
            raise TypeError("'actionkey' must be an instance of ActionKey")
        with self.ses.begin() as session:
            actionkey_db = self.get_actionkey(oid=actionkey.oid)[0]
            actionkey_db.action = actionkey.action
            actionkey_db.context = actionkey.context
            actionkey_db.decorator = actionkey.decorator
            actionkey_db.config = actionkey.config
            actionkey_db.target = actionkey.target
            actionkey_db.source = actionkey.source
            actionkey_db.referencedBehaviour = actionkey.referencedBehaviour
            actionkey_db.name = actionkey.name
            session.commit()

    # Begin methods for actionkey table

    # Begin methods for error table

    def save_error(self, error: Error, *args, **kwargs) -> "DBError":
        if not isinstance(error, Error):
            raise TypeError("'Error' must be an instance of Error")
        with self.ses.begin() as session:
            db_error = DBError()
            db_error.oid = error.oid
            db_error.name = error.name
            session.add(db_error)
            session.commit()
            return db_error

    def remove_error(self, error: Error, *args, **kwargs):
        if not isinstance(error, Error):
            raise TypeError("'Error' must be an instance of Error")
        with self.ses.begin() as session:
            error_db = self.get_error(oid=error.oid)[0]
            session.delete(error_db)
            session.commit()

    def get_error(
        self, name: Union["str", None] = None, oid: "str" = None, *args, **kwargs
    ) -> List[DBError]:
        with self.ses.begin() as session:
            query = session.query(DBError)

            if oid != None:
                query = query.filter(DBError.oid == oid)
            if name != None:
                query = query.filter(DBError.name == name)

            return query.all()

    def get_all_error(self, *args, **kwargs) -> list[DBError]:
        with self.ses.begin() as session:
            return session.query(DBError).all()

    def update_error(self, error: Error, *args, **kwargs):
        if not isinstance(error, Error):
            raise TypeError("'error' must be an instance of Error")
        with self.ses.begin() as session:
            error_db = self.get_error(oid=error.oid)[0]
            error_db.name = error.name
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
