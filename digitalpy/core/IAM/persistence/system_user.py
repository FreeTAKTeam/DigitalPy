"""this is the system user persistence file, containing the system user persistence class"""

from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

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
    uid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    token: Mapped[Optional[str]]
    password: Mapped[Optional[str]]
    device_type: Mapped[Optional[str]]
    certificate_package_name: Mapped[Optional[str]]

    # relationships
    system_user_groups: Mapped[List['SystemUserGroups']] = relationship(
        "SystemUserGroups", back_populates="system_user")
    
    users: Mapped['User'] = relationship("User", back_populates="system_user")

    api_calls: Mapped['ApiCalls'] = relationship("ApiCalls", back_populates="system_user")

    contact_uid: Mapped[Optional[str]] = mapped_column(ForeignKey(Contact.uid))
    contact: Mapped[Optional['Contact']] = relationship("Contact", back_populates="system_user")
    
    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, name={self.name}, token={self.token}, \
          password={self.password}, device_type={self.device_type}, \
          certificate_package_name={self.certificate_package_name}"
