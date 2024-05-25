"""this file contains the system group permission persistence class"""

from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING

from .iam_base import IAMBase

from .system_group import SystemGroup
from .permissions import Permissions

class SystemGroupPermission(IAMBase):
    """
    Represents a system group permission in the IAM component.
    
    Args:
        uid (String): the uid of the system group permission
        PermissionID (String): the PermissionID of the system group permission
    """

    __tablename__ = 'SystemGroupPermission'
    uid = Column(Text, primary_key=True)

    # relationships
    system_group_uid: Mapped[str] = mapped_column(ForeignKey('SystemGroup.uid'))
    system_group: Mapped["SystemGroup"] = relationship("SystemGroup", back_populates="system_group_permissions")

    permission_id: Mapped[str] = mapped_column(ForeignKey('Permissions.PermissionID'))
    permission: Mapped["Permissions"] = relationship("Permissions", back_populates="system_group_permissions")
