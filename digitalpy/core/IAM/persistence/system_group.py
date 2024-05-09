"""this file contains the persistency class for the system group table"""

from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import Text, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column

if TYPE_CHECKING:
    from digitalpy.core.IAM.persistence.system_group_permission import SystemGroupPermission
    from digitalpy.core.IAM.persistence.system_user_groups import SystemUserGroups

from .iam_base import IAMBase

class SystemGroup(IAMBase):
    """ this class represents a system group in the IAM component
    
    Args:
        uid (String): the uid of the system group
        name (String): the name of the system group
        description (String): the description of the system group
    """

    __tablename__ = 'SystemGroup'
    uid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]

    # relationships
    system_group_permissions: Mapped[List['SystemGroupPermission']] = relationship(back_populates="system_groups")

    system_user_groups: Mapped[List['SystemUserGroups']] = relationship(back_populates="system_groups")

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, name={self.name}, description={self.description}"