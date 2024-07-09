"""this file contains the permissions persistence class"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING, Optional

from .iam_base import IAMBase

class Permissions(IAMBase):
    """this class represents a permissions in the IAM component

    Args:
        PermissionID (String): the PermissionID of the permissions
        PermissionName (String): the PermissionName of the permissions
        PermissionDescription (String): the PermissionDescription of the permissions
        ResourceType (String): the ResourceType of the permissions
        CreateDate (String): the CreateDate of the permissions
        LastModifiedDate (String): the LastModifiedDate of the permissions
        IsActive (String): the IsActive of the permissions
    """
    __tablename__ = 'Permissions'
    PermissionID: Mapped[str] = mapped_column(primary_key=True)
    PermissionName: Mapped[str]
    PermissionDescription: Mapped[str]
    ResourceType: Mapped[Optional[str]]
    CreateDate: Mapped[Optional[str]]
    LastModifiedDate: Mapped[Optional[str]]
    IsActive: Mapped[Optional[str]]

    # relationships
    system_group_permissions: Mapped[list["SystemGroupPermission"]] = relationship(back_populates="permission")

    def __repr__(self) -> str:
        return super().__repr__() + f"PermissionID={self.PermissionID}, PermissionName={self.PermissionName}, PermissionDescription={self.PermissionDescription}, ResourceType={self.ResourceType}, CreateDate={self.CreateDate}, LastModifiedDate={self.LastModifiedDate}, IsActive={self.IsActive}"
