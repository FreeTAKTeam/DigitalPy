"""this file contains the session contact persistence class which is used to map the many to many 
relationship between a user and a session"""

from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .iam_base import IAMBase
from .session import Session
from .user import User

class SessionContact(IAMBase):
    """ this class represents a session contact in the IAM component
    
    Args:
        uid (String): the uid of the session contact
        session_uid (String): the session_uid of the session contact
        contact_uid (String): the contact_uid of the session contact
    """
    __tablename__ = 'SessionContact'
    uid: Mapped[str] = mapped_column(primary_key=True)
    
    # relationships
    session_uid: Mapped[str] = mapped_column(ForeignKey(Session.uid))
    sessions: Mapped["Session"] = relationship("Session", back_populates="session_contacts")

    contact_uid: Mapped[str] = mapped_column(ForeignKey(User.uid))
    users: Mapped["User"] = relationship("User", back_populates="session_contacts")

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, session_uid={self.session_uid}, contact_uid={self.contact_uid}"
