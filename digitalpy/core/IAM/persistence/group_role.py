from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .group import Group
from .role import Role
from . import IAMBase


class GroupRole(IAMBase): # pylint: disable=too-few-public-methods
    """ a mapping table between groups and roles.

    Args:
        id (int): The id of the group-role mapping.
        group (Group): The group of the mapping.
        role (Role): The role of the mapping.
    """
    __tablename__ = "group_role"

    id = Column(Integer, primary_key=True, autoincrement=True)

    group_id = Column(String, ForeignKey(Group.id))
    group: Group = relationship(Group, back_populates="roles")

    role_uid = Column(String, ForeignKey(Role.role_type))
    role: Role = relationship(Role, back_populates="groups")
