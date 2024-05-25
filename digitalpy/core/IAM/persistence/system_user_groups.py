"""this file contains the system user groups persistence class"""
from typing import TYPE_CHECKING
from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .iam_base import IAMBase
from .system_group import SystemGroup

if TYPE_CHECKING:
    from .system_user import SystemUser

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
    system_user_uid: Mapped[str] = mapped_column(ForeignKey("SystemUser.uid"))
    system_users: Mapped["SystemUser"] = relationship(
        "SystemUser", back_populates="system_user_groups")

    system_group_uid: Mapped[str] = mapped_column(ForeignKey(SystemGroup.uid))
    system_groups: Mapped["SystemGroup"] = relationship(
        "SystemGroup", back_populates="system_user_groups")

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, system_user_uid={self.system_user_uid}, system_group_uid={self.system_group_uid}"
