from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from . import IAMBase

if TYPE_CHECKING:
    from .role_permission import RolePermission

class Role(IAMBase):  # pylint: disable=too-few-public-methods
    """ The role of a user in the digitalpy system.

    Args:
        role_type (str): The type of the role.
        permissions (List['RolePermission']): The permissions of the role.
        missions (List['Mission']): The missions of the role.
    """
    __tablename__ = "Role"

    role_type = Column(String(100), primary_key=True)

    permissions: List['RolePermission'] = relationship(
        'RolePermission', back_populates="role")

    missions = relationship("Mission", back_populates="defaultRole")
