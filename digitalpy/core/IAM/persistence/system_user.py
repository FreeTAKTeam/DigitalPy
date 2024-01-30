"""this is the system user persistence file, containing the system user persistence class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship

from .iam_base import IAMBase
from .contact import Contact

if TYPE_CHECKING:
    from .user import User
    from .api_calls import ApiCalls
    from .system_user_groups import SystemUserGroups


class SystemUser(IAMBase):
    """
    Represents a system user in the IAM component.

    Args:
        uid (String): the uid of the system user
        name (String): the name of the system user
        token (String): the token of the system user
        password (String): the password of the system user
        group (String): the group of the system user
        device_type (String): the device type of the system user
        certificate_package_name (String): the certificate package name of the system user
    """

    __tablename__ = 'SystemUser'
    uid = Column(Text, primary_key=True)
    name = Column(Text, nullable=True)
    token = Column(Text, nullable=True)
    password = Column(Text, nullable=True)
    device_type = Column(Text, nullable=True)
    certificate_package_name = Column(Text, nullable=True)

    # relationships
    system_user_groups: List['SystemUserGroups'] = relationship(
        "SystemUserGroups", back_populates="system_users")
    
    users: 'User' = relationship("User", back_populates="system_user")

    api_calls: 'ApiCalls' = relationship("ApiCalls", back_populates="system_user")

    contact_uid = Column(Text, ForeignKey(Contact.uid))
    contact: Contact = relationship("Contact", back_populates="system_user")
    
    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, name={self.name}, token={self.token}, \
          password={self.password}, device_type={self.device_type}, \
          certificate_package_name={self.certificate_package_name}"
