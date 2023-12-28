from sqlalchemy import Column, Integer, String

from . import IAMBase

class User(IAMBase):
    """
    Represents a user in the IAM component.

    Args:
        id (int): the id of the user
        status (str): the status of the user
        service_id (str): the service id of the user
        protocol (str): the protocol of the user
    """

    __tablename__ = 'user'

    id = Column(String, primary_key=True)
    status = Column(String(50))
    service_id = Column(String(50))
    protocol = Column(String(50))

    def __repr__(self):
        return f"<User(id={self.id}, status={self.status}, service_id={self.service_id}, \
            protocol={self.protocol})>"
