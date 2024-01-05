"""this file contains the session persistence class"""

from sqlalchemy import Text, Column
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from . import IAMBase

if TYPE_CHECKING:
    from .session_contact import SessionContact

class Session(IAMBase):
    """ this class represents a session in the IAM component
    
    Args:
        uid (String): the uid of the session
        SessionStartTime (String): the SessionStartTime of the session
        SessionEndTime (String): the SessionEndTime of the session
        IPAddress (String): the IPAddress of the session
        ServiceName (String): the ServiceName of the session
    """
    __tablename__ = 'Session'
    uid = Column(Text, primary_key=True)
    SessionStartTime = Column(Text, nullable=True)
    SessionEndTime = Column(Text, nullable=True)
    IPAddress = Column(Text, nullable=True)
    ServiceName = Column(Text, nullable=True)

    # relationships
    session_contacts: 'SessionContact' = relationship("SessionContact", back_populates="sessions")

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, SessionStartTime={self.SessionStartTime}, SessionEndTime={self.SessionEndTime}, IPAddress={self.IPAddress}, ServiceName={self.ServiceName}"
