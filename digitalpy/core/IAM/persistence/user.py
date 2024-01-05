from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, List

from . import IAMBase
from .system_user import SystemUser
if TYPE_CHECKING:
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
    CoT_id = Column(Text, nullable=True)

    # relationships
    system_user_uid = Column(Text, ForeignKey(SystemUser.uid))
    system_user: SystemUser = relationship('SystemUser', back_populates='users')

    session_contacts: List['SessionContact'] = relationship('SessionContact', back_populates='users')

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, callsign={self.callsign}, CN={self.CN}, IP={self.IP}, CoT_id={self.CoT_id}"
