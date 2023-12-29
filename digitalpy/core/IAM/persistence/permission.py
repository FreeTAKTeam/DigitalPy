""" The permission of a user in the digitalpy system. """
from typing import List, TYPE_CHECKING
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from . import IAMBase

if TYPE_CHECKING:
    from .role_permission import RolePermission

class Permission(IAMBase): # pylint: disable=too-few-public-methods
    """ The permission of a user in the digitalpy system.

    Args:
        permission_type (str): The type of the permission.
        roles (List['RolePermission']): The roles of the permission.
    """
    __tablename__ = "permission"

    permission_type: str = Column(String(100), primary_key=True) # type: ignore

    roles : List['RolePermission'] = relationship('RolePermission', back_populates="permission")
