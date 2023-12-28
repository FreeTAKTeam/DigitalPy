from typing import TYPE_CHECKING
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from digitalpy.core.IAM.persistence.user import User
from digitalpy.core.main.controller import Controller
from ..persistence import IAMBase
from ..configuration.iam_constants import DB_PATH
if TYPE_CHECKING:
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.action_mapper import ActionMapper


class IAMPersistenceController(Controller):
    """this class is responsible for handling the persistence of the IAM
    component. It is responsible for creating, removing and retrieving
    users from the IAM system.

    Args:
        request (Request): the request object
        response (Response): the response object
        sync_action_mapper (ActionMapper): the action mapper
        configuration (Configuration): the configuration object
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

        IAMBase.metadata.create_all(engine)

        # create a Session
        return SessionClass()

    def save_user(self, user: User, *args, **kwargs):
        """this function is responsible for creating a user in the IAM
        system. The user is created with a default group and a default
        permission set.

        Args:
            user (NetworkClient): the user to be created
        """
        if not isinstance(user, User):
            raise TypeError("'user' must be an instance of NetworkClient")
        self.ses.add(user)
        self.ses.commit()

    def remove_user(self, user: User, *args, **kwargs):
        """this function is responsible for removing a user from the IAM
        system.

        Args:
            user (NetworkClient): the user to be removed
        """
        if not isinstance(user, User):
            raise TypeError("'user' must be an instance of NetworkClient")
        self.ses.delete(user)
        self.ses.commit()

    def get_user(self, user_id: str, *args, **kwargs) -> User:
        """this function is responsible for getting a user from the IAM
        system.

        Args:
            user_id (str): the id of the user to be retrieved

        Returns:
            User: the user retrieved
        """
        if not isinstance(user_id, str):
            raise TypeError("'user_id' must be an instance of str")
        return self.ses.query(User).filter(User.id == user_id).first()

    def get_all_users(self, *args, **kwargs) -> list[User]:
        """this function is responsible for getting all users from the IAM
        system.

        Returns:
            list[User]: a list of all users
        """
        return self.ses.query(User).all()

    def clear_users(self, *args, **kwargs):
        """this function is responsible for clearing all users from the IAM
        system.
        """
        self.ses.query(User).delete()
        self.ses.commit()

    def __getstate__(self) -> object:
        state: dict = super().__getstate__()  # type: ignore
        if "ses" in state:
            del state["ses"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.ses = self.create_db_session()
