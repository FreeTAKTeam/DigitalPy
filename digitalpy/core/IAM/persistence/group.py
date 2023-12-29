"""This module contains the Group class."""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from . import IAMBase


class Group(IAMBase): # pylint: disable=too-few-public-methods
    """
    Represents a group in the IAM component.

    Args:
        id (int): the id of the group
        status (str): the status of the group
        service_id (str): the service id of the group
        protocol (str): the protocol of the group
    """

    __tablename__ = 'group'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    users = relationship("user", back_populates="group")
    roles = relationship("role", back_populates="group")