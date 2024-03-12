"""this file contains the system user groups persistence class"""
from typing import TYPE_CHECKING
from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship

from .iam_base import IAMBase
from .system_group import SystemGroup

class SystemUserGroups(IAMBase):
    """
    Represents a system user groups in the IAM component.

    Args:
        uid (String): the uid of the system user groups
        system_user_uid (String): the system_user_uid of the system user groups
        system_group_uid (String): the system_group_uid of the system user groups
    """

    __tablename__ = 'SystemUserGroups'
    uid = Column(Text, primary_key=True)

    # relationships
    system_user_uid = Column(Text, ForeignKey("SystemUser.uid"))
    system_users = relationship(
        "SystemUser", back_populates="system_user_groups")

    system_group_uid = Column(Text, ForeignKey(SystemGroup.uid))
    system_groups: SystemGroup = relationship(
        "SystemGroup", back_populates="system_user_groups")

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, system_user_uid={self.system_user_uid}, system_group_uid={self.system_group_uid}"
