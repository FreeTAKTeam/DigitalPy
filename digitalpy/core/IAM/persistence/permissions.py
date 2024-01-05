"""this file contains the permissions persistence class"""

from sqlalchemy import Text, Column
from sqlalchemy.orm import relationship

from . import IAMBase

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
    PermissionID = Column(Text, primary_key=True)
    PermissionName = Column(Text, nullable=True)
    PermissionDescription = Column(Text, nullable=True)
    ResourceType = Column(Text, nullable=True)
    CreateDate = Column(Text, nullable=True)
    LastModifiedDate = Column(Text, nullable=True)
    IsActive = Column(Text, nullable=True)

    # relationships
    system_group_permissions = relationship("SystemGroupPermission", back_populates="permissions")

    def __repr__(self) -> str:
        return super().__repr__() + f"PermissionID={self.PermissionID}, PermissionName={self.PermissionName}, PermissionDescription={self.PermissionDescription}, ResourceType={self.ResourceType}, CreateDate={self.CreateDate}, LastModifiedDate={self.LastModifiedDate}, IsActive={self.IsActive}"
