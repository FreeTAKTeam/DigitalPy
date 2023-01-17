from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import registry, sessionmaker, Session

from digitalpy.core.persistence.impl.sqlalchemy_persistent_object import SQLAlchemyPersistentObject
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.persistence.controllers.persistence_controller import PersistenceController

class SQLAlchemyPersistenceController(PersistenceController):

    def __init__(self, request: Request, response: Response, action_mapper: ActionMapper, configuration: Configuration, connection_string: str):
        super().__init__(request, response, action_mapper, configuration)
        self.connection_string = connection_string

    def initialize_connection(self):
        """initialize connection to sql alchemy database
        """
        self.registry = registry()
        self.base = self.registry.generate_base()
        self.engine = self.create_engine()
        self.session_maker = sessionmaker(self.engine)
        
        # listen for the map_imperatively function to be called and attempt
        # to add the newly created tables when it is. this is done because
        # class' are loaded dynamically
        #listen(self.registry, "map_imperatively", self.create_database)

    def _get_session(self) -> Session:
        """get an sqlalchemy session instance

        Returns:
            Session: a session instance with the database
        """
        return self.session_maker()

    def create_engine(self):
        """
        this function creates the engine and applies all the metadata
        of classes which inherit the base class and applies it to the database
        to create tables.
        :arg
        """
        engine = create_engine(self.connection_string, echo=False)
        if inspect(engine).has_table("SystemUser") == False:
            self.create_database(engine)
            return engine
        else:
            return engine
    
    def create_database(self, engine):
        self.base.metadata.create_all(engine)
        return engine

    def save(self, persitent_object: SQLAlchemyPersistentObject) -> bool:
        """save the given persistent_object to the database

        Args:
            persitent_object (SQLAlchemyPersistentObject): _description_
        """
        with self._get_session() as ses:
            ses.add(persitent_object)