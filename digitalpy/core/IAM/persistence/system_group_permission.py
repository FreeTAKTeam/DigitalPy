"""this file contains the system group permission persistence class"""

from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship

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
    system_group_uid = Column(Text, ForeignKey(SystemGroup.uid))
    system_groups = relationship("SystemGroup", back_populates="system_group_permissions")

    permission_id = Column(Text, ForeignKey(Permissions.PermissionID))
    permissions: Permissions = relationship("Permissions", back_populates="system_group_permissions")
