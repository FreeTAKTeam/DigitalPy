"""the api calls for IAM persistence"""

from sqlalchemy import Text, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, Optional

from .system_user import SystemUser
from .iam_base import IAMBase

class ApiCalls(IAMBase):
    """
    Represents a api call in the IAM component.

    Args:
        uid (String): the uid of the api call
        call_id (int): the call_id of the api call
        content (String): the content of the api call
        endpoint (String): the endpoint of the api call
        timestamp (String): the timestamp of the api call
        user_id (String): the user_id of the api call
    """

    __tablename__ = 'APICalls'
    call_id: Mapped[int] = Column(Integer, primary_key=True)
    content: Mapped[Optional[str]]
    endpoint: Mapped[Optional[str]]
    timestamp: Mapped[Optional[str]]

    # relationships
    system_user_uid: Mapped[str] = mapped_column(ForeignKey(SystemUser.uid))
    system_user: Mapped['SystemUser'] = relationship('SystemUser', back_populates='api_calls')

    def __repr__(self) -> str:
        return super().__repr__() + f"call_id={self.call_id}, content={self.content}, endpoint={self.endpoint}, timestamp={self.timestamp}, system_user_uid={self.system_user_uid}"