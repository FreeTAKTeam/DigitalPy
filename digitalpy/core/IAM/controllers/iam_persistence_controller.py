import os
from typing import TYPE_CHECKING
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

# import tables in initialization order
from digitalpy.core.IAM.persistence.session_contact import SessionContact
from digitalpy.core.IAM.persistence.system_group_permission import SystemGroupPermission
from digitalpy.core.IAM.persistence.system_user_groups import SystemUserGroups
from digitalpy.core.IAM.persistence.system_group import SystemGroup
from digitalpy.core.IAM.persistence.system_user import SystemUser
from digitalpy.core.IAM.persistence.user import User
from digitalpy.core.IAM.persistence.session import Session as DBSession
from digitalpy.core.IAM.persistence.api_calls import ApiCalls
from digitalpy.core.IAM.persistence.contact import Contact
from digitalpy.core.network.domain.client_status import ClientStatus

from digitalpy.core.IAM.persistence.permissions import Permissions

from digitalpy.core.main.controller import Controller
from ..persistence.iam_base import IAMBase
from ..configuration.iam_constants import (
    AUTHENTICATED_USERS,
    UNAUTHENTICATED_USERS,
    ADMIN_USERS,
    DB_PATH,
)

if TYPE_CHECKING:
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.domain.model.configuration import (
        Configuration,
    )
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

    # create the engine as a class variable to avoid creating it multiple times
    # implementation ref https://docs.sqlalchemy.org/en/20/core/pooling.html#using-connection-pools-with-multiprocessing-or-os-fork
    engine = None
    engine_pid = None

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
        # create a Session
        return SessionClass()

    def intialize_db(self):
        """create the tables in the database"""
        # use NullPool to prevent connections from remaning open, this allows
        # us to delete the component and it's database at runtime (component management)
        engine = create_engine(DB_PATH, poolclass=NullPool)
        IAMBase.metadata.create_all(engine, checkfirst=True)

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

    def get_user_by_cn(self, cn: str, *args, **kwargs) -> list[User]:
        """this function is responsible for getting a user from the IAM
        system.

        Args:
            cn (str): the common name of the user to be retrieved

        Returns:
            list[User]: the user retrieved
        """
        if not isinstance(cn, str):
            raise TypeError("'user_name' must be an instance of str")
        return self.ses.query(User).filter(User.CN == cn)

    def get_all_users(self, *args, **kwargs) -> list[User]:
        """this function is responsible for getting all users from the IAM
        system.

        Returns:
            list[User]: a list of all users
        """
        return self.ses.query(User).all()

    def clear_sessions(self, *args, **kwargs):
        """this function is responsible for clearing all sessions from the IAM
        system.
        """
        self.ses.query(SessionContact).delete()
        self.ses.query(DBSession).delete()
        self.ses.commit()

    def remove_session(self, session: DBSession, *args, **kwargs):
        """this function is responsible for removing a session from the IAM
        system.

        Args:
            session (Session): the session to be removed
        """
        if not isinstance(session, DBSession):
            raise TypeError("'session' must be an instance of Session")
        for ses_con in session.session_contacts:
            self.ses.delete(ses_con)
        self.ses.delete(session)
        self.ses.commit()

    def save_session(self, session: DBSession, user: User, *args, **kwargs):
        """this function is responsible for saving a session in the IAM
        system.

        Args:
            session (Session): the session to be saved
        """
        if not isinstance(session, DBSession):
            raise TypeError("'session' must be an instance of Session")
        self.ses.add(session)
        self.ses.commit()

        ses_con = SessionContact(uid=str(uuid.uuid4()), session=session, user=user)
        self.ses.add(ses_con)
        self.ses.commit()

    def get_all_sessions(self, *args, **kwargs) -> list[DBSession]:
        """this function is responsible for getting all sessions from the IAM
        system.

        Returns:
            list[Session]: a list of all sessions
        """
        return self.ses.query(DBSession).all()

    def get_session_by_uid(self, oid: str, *args, **kwargs) -> DBSession:
        """this function is responsible for getting a session from the IAM
        system.

        Args:
            oid (str): the object id of the session to be retrieved

        Returns:
            Session: the session retrieved
        """
        if not isinstance(oid, str):
            raise TypeError("'oid' must be an instance of str")
        return self.ses.query(DBSession).filter(DBSession.uid == oid).first()

    def create_default_permissions(self, *args, **kwargs) -> list[Permissions]:
        """this function is responsible for creating the default permissions in the IAM

        Returns:
            list[Permissions]: a list of the default permissions created
        """
        permissions = []
        # TODO: add more permissions
        if (
            self.ses.query(Permissions)
            .filter(Permissions.PermissionName == "receiveData")
            .first()
            is None
        ):
            recvDataPerm = Permissions(
                PermissionID=str(uuid.uuid4()),
                PermissionName="receiveData",
                PermissionDescription="Receive data",
            )
            self.ses.add(recvDataPerm)
            self.ses.commit()
            permissions.append(recvDataPerm)
        if (
            self.ses.query(Permissions)
            .filter(Permissions.PermissionName == "requestStandardAction")
            .first()
            is None
        ):
            reqStdActionPerm = Permissions(
                PermissionID=str(uuid.uuid4()),
                PermissionName="requestStandardAction",
                PermissionDescription="Request a standard action",
            )
            self.ses.add(reqStdActionPerm)
            self.ses.commit()
            permissions.append(reqStdActionPerm)
        if (
            self.ses.query(Permissions)
            .filter(Permissions.PermissionName == "requestCoreAction")
            .first()
            is None
        ):
            reqCoreActionPerm = Permissions(
                PermissionID=str(uuid.uuid4()),
                PermissionName="requestCoreAction",
                PermissionDescription="Request a core action",
            )
            self.ses.add(reqCoreActionPerm)
            self.ses.commit()
            permissions.append(reqCoreActionPerm)
        return permissions

    def create_default_groups(self, *args, **kwargs) -> list[SystemGroup]:
        """this function is responsible for creating the default groups in the IAM

        Returns:
            list[SystemGroup]: a list of the default groups created
        """
        groups = []

        self._create_authenticated_user_group(groups)

        self._create_admin_user_group(groups)

        self._create_unauthenticated_user_group(groups)

        return groups

    def _create_admin_user_group(self, groups: list[SystemGroup]):
        """this function is responsible for creating the admin user group in the IAM

        Args:
            groups (list[SystemGroup]): the list of groups to append the created group to
        """
        if self.get_group_by_name(ADMIN_USERS):
            groups.append(self.get_group_by_name(ADMIN_USERS))
        else:
            group = SystemGroup(
                uid=str(uuid.uuid4()),
                name=ADMIN_USERS,
            )
            self.ses.add(group)
            self.ses.commit()
            rcvDataGrp = SystemGroupPermission(
                uid=str(uuid.uuid4()),
                system_group=group,
                permission=self.ses.query(Permissions)
                .filter(Permissions.PermissionName == "receiveData")
                .first(),
            )
            self.ses.add(rcvDataGrp)
            self.ses.commit()
            rqstStdAct = SystemGroupPermission(
                uid=str(uuid.uuid4()),
                system_group=group,
                permission=self.ses.query(Permissions)
                .filter(Permissions.PermissionName == "requestStandardAction")
                .first(),
            )
            self.ses.add(rqstStdAct)
            self.ses.commit()
            rqstCoreActGrpPerm = SystemGroupPermission(
                uid=str(uuid.uuid4()),
                system_group=group,
                permission=self.ses.query(Permissions)
                .filter(Permissions.PermissionName == "requestCoreAction")
                .first(),
            )
            self.ses.add(rqstCoreActGrpPerm)
            self.ses.commit()

    def _create_unauthenticated_user_group(self, groups: list[SystemGroup]):
        """this function is responsible for creating the unauthenticated user group in the IAM

        Args:
            groups (list[SystemGroup]): the list of groups to append the created group to
        """
        if self.get_group_by_name(UNAUTHENTICATED_USERS):
            groups.append(self.get_group_by_name(UNAUTHENTICATED_USERS))
        else:
            group = SystemGroup(
                uid=str(uuid.uuid4()),
                name=UNAUTHENTICATED_USERS,
            )
            self.ses.add(group)
            self.ses.commit()
            groups.append(group)

    def _create_authenticated_user_group(self, groups: list[SystemGroup]):
        """this function is responsible for creating the authenticated user group in the IAM

        Args:
            groups (list[SystemGroup]): the list of groups to append the created group to
        """
        if self.get_group_by_name(AUTHENTICATED_USERS):
            groups.append(self.get_group_by_name(AUTHENTICATED_USERS))
        else:
            group = SystemGroup(
                uid=str(uuid.uuid4()),
                name=AUTHENTICATED_USERS,
            )
            self.ses.add(group)
            self.ses.commit()
            rcvDataGrp = SystemGroupPermission(
                uid=str(uuid.uuid4()),
                system_group=group,
                permission=self.ses.query(Permissions)
                .filter(Permissions.PermissionName == "receiveData")
                .first(),
            )
            self.ses.add(rcvDataGrp)
            self.ses.commit()
            rqstStdAct = SystemGroupPermission(
                uid=str(uuid.uuid4()),
                system_group=group,
                permission=self.ses.query(Permissions)
                .filter(Permissions.PermissionName == "requestStandardAction")
                .first(),
            )
            self.ses.add(rqstStdAct)
            self.ses.commit()

    def create_admin_system_user(self, *args, **kwargs) -> SystemUser:
        """this function is responsible for creating a default system user in the IAM
        system.

        Returns:
            SystemUser: the system user created
        """
        if self.get_system_user_by_name("Administrator"):
            self.ses.close()
            return self.get_system_user_by_name("Administrator")
        # create the administator system user
        admin_sysuser = SystemUser(
            uid=str(uuid.uuid4()),
            name="Administrator",
            token="admin",
            password="admin",
            device_type="admin",
            certificate_package_name="admin",
        )
        self.ses.add(admin_sysuser)
        self.ses.commit()
        # get the groups
        authed_users = self.get_group_by_name(AUTHENTICATED_USERS)
        admin_users = self.get_group_by_name(ADMIN_USERS)
        # create the admin user
        admin_usr = User(
            uid=str(uuid.uuid4()),
            callsign="Administrator",
            system_user=admin_sysuser,
            CN="Administrator",
            status=ClientStatus.DISCONNECTED.value,
        )
        self.ses.add(admin_usr)
        self.ses.commit()

        # create the system user groups
        admin_usr_grps = SystemUserGroups(
            uid=str(uuid.uuid4()), system_user=admin_sysuser, system_group=admin_users
        )
        self.ses.add(admin_usr_grps)
        self.ses.commit()
        authed_usr_grps = SystemUserGroups(
            uid=str(uuid.uuid4()), system_user=admin_sysuser, system_group=authed_users
        )
        self.ses.add(authed_usr_grps)
        self.ses.commit()
        self.ses.close()
        return admin_sysuser

    def create_anonymous_system_user(self, *args, **kwargs) -> SystemUser:
        """this function is responsible for creating an anonymous system user in the IAM
        system used for unauthenticated sessions.

        Returns:
            SystemUser: the system user created
        """
        if self.get_system_user_by_name("Anonymous"):
            self.ses.close()
            return self.get_system_user_by_name("Anonymous")

        anon_sysuser = SystemUser(
            uid=str(uuid.uuid4()),
            name="Anonymous",
            token="anonymous",
            password="anonymous",
            device_type="anonymous",
            certificate_package_name="anonymous",
        )
        self.ses.add(anon_sysuser)
        self.ses.commit()

        anon_user = User(
            uid=str(uuid.uuid4()),
            callsign="Anonymous",
            system_user=anon_sysuser,
            CN="Anonymous",
            status=ClientStatus.DISCONNECTED.value,
        )
        self.ses.add(anon_user)
        self.ses.commit()

        unauthed_users = self.get_group_by_name(UNAUTHENTICATED_USERS)
        unauth_sysgrp = SystemUserGroups(
            uid=str(uuid.uuid4()), system_user=anon_sysuser, system_group=unauthed_users
        )
        self.ses.add(unauth_sysgrp)
        self.ses.commit()
        self.ses.close()
        return anon_sysuser

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
        return (
            self.ses.query(SystemGroup).filter(SystemGroup.name == group_name).first()
        )

    def get_all_groups(self, *args, **kwargs) -> list[SystemGroup]:
        """this function is responsible for getting all groups from the IAM
        system.

        Returns:
            list[SystemUserGroups]: a list of all groups
        """
        return self.ses.query(SystemGroup).all()

    def create_group_permission(
        self, group_permission: SystemGroupPermission, *args, **kwargs
    ):
        """this function is responsible for creating a group permission in the IAM
        system.

        Args:
            group_permission (SystemGroupPermission): the group permission to be created
        """
        if not isinstance(group_permission, SystemGroupPermission):
            raise TypeError(
                "'group_permission' must be an instance of SystemGroupPermission"
            )
        self.ses.add(group_permission)
        self.ses.commit()

    def get_all_system_users(self, *args, **kwargs) -> list[SystemUser]:
        """this function is responsible for getting all system users from the IAM
        system.

        Returns:
            list[SystemUser]: a list of all system users
        """
        return self.ses.query(SystemUser).all()

    def get_system_user_by_name(
        self, system_user_name: str, *args, **kwargs
    ) -> SystemUser:
        """this function is responsible for creating a system user in the IAM
        system.

        Args:
            system_user (SystemUser): the system user to be created
        """
        if not isinstance(system_user_name, str):
            raise TypeError("'system_user' must be an instance of SystemUser")
        sys_user = (
            self.ses.query(SystemUser)
            .filter(SystemUser.name == system_user_name)
            .first()
        )
        self.ses.close()
        return sys_user

    def add_user_to_system_user(
        self, user: User, system_user: SystemUser, *args, **kwargs
    ):
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
        """return the state of the object, removing the session and engine object"""
        state: dict = super().__getstate__()  # type: ignore
        if "ses" in state:
            del state["ses"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.ses = self.create_db_session()
