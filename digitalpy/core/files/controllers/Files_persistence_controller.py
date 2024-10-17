from typing import TYPE_CHECKING, List, Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

# import tables in initialization order
from digitalpy.core.files.persistence.folder import Folder as DBFolder
from digitalpy.core.files.persistence.file import File as DBFile
from digitalpy.core.files.persistence.error import Error as DBError

# import domain model classes
from digitalpy.core.files.domain.model.folder import Folder
from digitalpy.core.files.domain.model.file import File
from digitalpy.core.files.domain.model.error import Error

from digitalpy.core.main.controller import Controller
from digitalpy.core.files.persistence.Files_base import FilesBase
from digitalpy.core.files.configuration.Files_constants import DB_PATH

if TYPE_CHECKING:
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.action_mapper import ActionMapper


class FilesPersistenceController(Controller):
    """this class is responsible for handling the persistence of the Files
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
        # use NullPool to prevent connections from remaning open, this allows
        # us to delete the component and it's database at runtime (component management)
        engine = create_engine(DB_PATH, poolclass=NullPool)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine, expire_on_commit=False)

        FilesBase.metadata.create_all(engine)

        # create a Session
        return SessionClass

    # Begin methods for folder table


    def save_folder(self, folder: Folder, *args, **kwargs) -> 'DBFolder':
        if not isinstance(folder, Folder):
            raise TypeError("'Folder' must be an instance of Folder")
        with self.ses.begin() as session:
            db_folder = DBFolder()
            db_folder.oid = folder.oid
            db_folder.path = folder.path
            db_folder.size = folder.size
            db_folder.permissions = folder.permissions
            db_folder.name = folder.name
            session.add(db_folder)
            session.commit()
            return db_folder


    def remove_folder(self, folder: Folder, *args, **kwargs):
        if not isinstance(folder, Folder):
            raise TypeError("'Folder' must be an instance of Folder")
        with self.ses.begin() as session:
            folder_db = self.get_folder(oid=folder.oid)[0]
            session.delete(folder_db)
            session.commit()

    def get_folder(self, path:Union['str', None] = None, size:Union['float', None] = None, permissions:Union['str', None] = None, name:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBFolder]:
        with self.ses.begin() as session:
            query = session.query(DBFolder)

            if oid != None:
                query = query.filter(DBFolder.oid == oid)
            if path != None:
                query = query.filter(DBFolder.path == path)
            if size != None:
                query = query.filter(DBFolder.size == size)
            if permissions != None:
                query = query.filter(DBFolder.permissions == permissions)
            if name != None:
                query = query.filter(DBFolder.name == name)

            return query.all()


    def get_all_folder(self, *args, **kwargs) -> list[DBFolder]:
        with self.ses.begin() as session:
            return session.query(DBFolder).all()

    def update_folder(self, folder: Folder, *args, **kwargs):
        if not isinstance(folder, Folder):
            raise TypeError("'folder' must be an instance of Folder")
        with self.ses.begin() as session:
            folder_db = self.get_folder(oid = folder.oid)[0]
            folder_db.path = folder.path
            folder_db.size = folder.size
            folder_db.permissions = folder.permissions
            folder_db.name = folder.name
            session.commit()

    # Begin methods for folder table

    # Begin methods for file table


    def save_file(self, file: File, *args, **kwargs) -> 'DBFile':
        if not isinstance(file, File):
            raise TypeError("'File' must be an instance of File")
        with self.ses.begin() as session:
            db_file = DBFile()
            db_file.oid = file.oid
            db_file.path = file.path
            db_file.permissions = file.permissions
            db_file.size = file.size
            db_file.name = file.name
            session.add(db_file)
            session.commit()
            return db_file


    def remove_file(self, file: File, *args, **kwargs):
        if not isinstance(file, File):
            raise TypeError("'File' must be an instance of File")
        with self.ses.begin() as session:
            file_db = self.get_file(oid=file.oid)[0]
            session.delete(file_db)
            session.commit()

    def get_file(self, path:Union['str', None] = None, permissions:Union['str', None] = None, size:Union['float', None] = None, name:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBFile]:
        with self.ses.begin() as session:
            query = session.query(DBFile)

            if oid != None:
                query = query.filter(DBFile.oid == oid)
            if path != None:
                query = query.filter(DBFile.path == path)
            if permissions != None:
                query = query.filter(DBFile.permissions == permissions)
            if size != None:
                query = query.filter(DBFile.size == size)
            if name != None:
                query = query.filter(DBFile.name == name)

            return query.all()


    def get_all_file(self, *args, **kwargs) -> list[DBFile]:
        with self.ses.begin() as session:
            return session.query(DBFile).all()

    def update_file(self, file: File, *args, **kwargs):
        if not isinstance(file, File):
            raise TypeError("'file' must be an instance of File")
        with self.ses.begin() as session:
            file_db = self.get_file(oid = file.oid)[0]
            file_db.path = file.path
            file_db.permissions = file.permissions
            file_db.size = file.size
            file_db.name = file.name
            session.commit()

    # Begin methods for file table

    # Begin methods for error table


    def save_error(self, error: Error, *args, **kwargs) -> 'DBError':
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

    def get_error(self, name:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBError]:
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
            error_db = self.get_error(oid = error.oid)[0]
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
