from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List

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
    uid = Column(Text, primary_key=True)
    callsign = Column(Text, nullable=True)
    CN = Column(Text, nullable=True)
    IP = Column(Text, nullable=True)
    protocol = Column(Text, nullable=False)
    service_id = Column(Text, nullable=False)
    status = Column(Text)
    # relationships
    system_user_uid = Column(Text, ForeignKey("SystemUser.uid"))
    system_user: 'SystemUser' = relationship('SystemUser', back_populates='users')

    session_contacts: List['SessionContact'] = relationship('SessionContact', back_populates='users')

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, callsign={self.callsign}, CN={self.CN}, IP={self.IP}, service_id={self.service_id}"
