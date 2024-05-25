"""this file contains the session persistence class"""

from sqlalchemy import Text, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, Optional

from .iam_base import IAMBase

if TYPE_CHECKING:
    from .session_contact import SessionContact

class Session(IAMBase):
    """ this class represents a session in the IAM component
    
    Args:
        uid (String): the uid of the session
        SessionStartTime (String): the SessionStartTime of the session
        SessionEndTime (String): the SessionEndTime of the session
        IPAddress (String): the IPAddress of the session
        ServiceId (String): the id of the service associated with the session
    """
    __tablename__ = 'Session'
    uid: Mapped[str] = mapped_column(primary_key=True)
    SessionStartTime: Mapped[Optional[str]]
    SessionEndTime: Mapped[Optional[str]]
    IPAddress: Mapped[Optional[str]]
    ServiceId: Mapped[Optional[str]]
    protocol: Mapped[Optional[str]]

    # relationships
    session_contacts: Mapped['SessionContact'] = relationship("SessionContact", back_populates="sessions")

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, SessionStartTime={self.SessionStartTime}, SessionEndTime={self.SessionEndTime}, IPAddress={self.IPAddress}, ServiceName={self.ServiceName}"
