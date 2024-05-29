from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import TYPE_CHECKING, List, Optional

from .iam_base import IAMBase

if TYPE_CHECKING:
    from digitalpy.core.IAM.persistence.system_user import SystemUser
    from .session_contact import SessionContact

class User(IAMBase):
    """
    Represents a user in the IAM component.

    Args:
        id (int): the id of the user
        status (str): the status of the user
        service_id (str): the service id of the user
        protocol (str): the protocol of the user
    """

    __tablename__ = 'User'
    uid: Mapped[str] = mapped_column(primary_key=True)
    callsign: Mapped[Optional[str]]
    CN: Mapped[Optional[str]]
    status: Mapped[str]
    # relationships
    system_user_uid: Mapped[str] = mapped_column(ForeignKey("SystemUser.uid"))
    system_user: Mapped['SystemUser'] = relationship('SystemUser', back_populates='users')

    session_contacts: Mapped[List['SessionContact']] = relationship('SessionContact', back_populates='user')

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, callsign={self.callsign}, CN={self.CN}"
