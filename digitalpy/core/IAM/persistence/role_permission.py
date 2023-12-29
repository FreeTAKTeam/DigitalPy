from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import IAMBase
from .permission import Permission
from .role import Role

class RolePermission(IAMBase): # pylint: disable=too-few-public-methods
    """ a mapping table between roles and permissions.

    Args:
        id (int): The id of the role-permission mapping.
        permission (Permission): The permission of the mapping.
        role (Role): The role of the mapping.
    """
    __tablename__ = "role_permission"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    permission_id = Column(String, ForeignKey(Permission.permission_type))
    permission: Permission = relationship(Permission, back_populates="roles")
    
    role_uid = Column(String, ForeignKey(Role.role_type))
    role : Role = relationship(Role, back_populates="permissions")