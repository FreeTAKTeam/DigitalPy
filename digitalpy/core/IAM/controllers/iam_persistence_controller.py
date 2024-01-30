from typing import TYPE_CHECKING
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# import tables in initialization order
from digitalpy.core.IAM.persistence.session_contact import SessionContact
from digitalpy.core.IAM.persistence.system_group_permission import SystemGroupPermission
from digitalpy.core.IAM.persistence.system_user_groups import SystemUserGroups
from digitalpy.core.IAM.persistence.system_group import SystemGroup
from digitalpy.core.IAM.persistence.system_user import SystemUser
from digitalpy.core.IAM.persistence.user import User
from digitalpy.core.IAM.persistence.api_calls import ApiCalls
from digitalpy.core.IAM.persistence.contact import Contact

from digitalpy.core.IAM.persistence.permissions import Permissions

from digitalpy.core.main.controller import Controller
from ..persistence.iam_base import IAMBase
from ..configuration.iam_constants import AUTHENTICATED_USERS, DB_PATH
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
        permissions set.

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
        return self.ses.query(User).filter(User.uid == user_id).first()

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

    def create_default_system_user(self, *args, **kwargs) -> SystemUser:
        """this function is responsible for creating a default system user in the IAM
        system.

        Returns:
            SystemUser: the system user created
        """
        if self.get_system_user_by_name("default"):
            return self.get_system_user_by_name("default")
        
        system_user = SystemUser(
            uid="default",
            name="default",
            token="default",
            password="default",
            device_type="default",
            certificate_package_name="default",
        )
        authed_users = self.get_group_by_name(AUTHENTICATED_USERS)
        system_user_groups = SystemUserGroups(
            uid="default",
            system_groups=authed_users,
            system_users=system_user,
        )
        system_user.system_user_groups.append(system_user_groups)
        self.ses.add(system_user_groups)
        self.ses.add(system_user)
        self.ses.commit()
        return system_user

    def create_permission(self, permission: Permissions, *args, **kwargs):
        """this function is responsible for creating a permission in the IAM
        system.

        Args:
            permissions (Permissions): the permission to be created
        """
        if not isinstance(permission, Permissions):
            raise TypeError("'permissions' must be an instance of Permissions")
        self.ses.add(permission)
        self.ses.commit()

    def create_group(self, group: SystemGroup, *args, **kwargs):
        """this function is responsible for creating a group in the IAM
        system.

        Args:
            group (SystemUserGroups): the group to be created
        """
        if not isinstance(group, SystemGroup):
            raise TypeError("'group' must be an instance of SystemUserGroups")
        self.ses.add(group)
        self.ses.commit()

    def get_group_by_name(self, group_name: str, *args, **kwargs) -> SystemGroup:
        """this function is responsible for getting a group from the IAM
        system.

        Args:
            group_name (str): the name of the group to be retrieved

        Returns:
            SystemUserGroups: the group retrieved
        """
        if not isinstance(group_name, str):
            raise TypeError("'group_name' must be an instance of str")
        return self.ses.query(SystemGroup).filter(SystemGroup.name == group_name).first()

    def create_group_permission(self, group_permission: SystemGroupPermission, *args, **kwargs):
        """this function is responsible for creating a group permission in the IAM
        system.

        Args:
            group_permission (SystemGroupPermission): the group permission to be created
        """
        if not isinstance(group_permission, SystemGroupPermission):
            raise TypeError("'group_permission' must be an instance of SystemGroupPermission")
        self.ses.add(group_permission)
        self.ses.commit()

    def get_system_user_by_name(self, system_user_name: str, *args, **kwargs) -> SystemUser:
        """this function is responsible for creating a system user in the IAM
        system.

        Args:
            system_user (SystemUser): the system user to be created
        """
        if not isinstance(system_user_name, str):
            raise TypeError("'system_user' must be an instance of SystemUser")
        return self.ses.query(SystemUser).filter(SystemUser.name == system_user_name).first()

    def add_user_to_system_user(self, user: User, system_user: SystemUser, *args, **kwargs):
        """this function is responsible for adding a user to a system user in the IAM
        system.

        Args:
            user (User): the user to be added
            system_user (SystemUser): the system user to be added to
        """
        if not isinstance(user, User):
            raise TypeError("'user' must be an instance of User")
        if not isinstance(system_user, SystemUser):
            raise TypeError("'system_user' must be an instance of SystemUser")
        system_user.users.append(user)
        user.system_user = system_user
        self.ses.commit()

    def __getstate__(self) -> object:
        state: dict = super().__getstate__()  # type: ignore
        if "ses" in state:
            del state["ses"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.ses = self.create_db_session()
