"""this file contains the contact persistence class"""

from sqlalchemy import Text, Column, ForeignKey
from sqlalchemy.orm import relationship

from . import IAMBase

class Contact(IAMBase):
    """
    Represents a contact in the IAM component.
    
    Args:
        uid (String): the uid of the contact
        callsign (String): the callsign of the contact
        iconsetpath (String): the iconsetpath of the contact
        sipAddress (String): the sipAddress of the contact
        emailAddress (String): the emailAddress of the contact
        xmppUsername (String): the xmppUsername of the contact
        endpoint (String): the endpoint of the contact
        name (String): the name of the contact
        phone (String): the phone of the contact
    """

    __tablename__ = 'Contact'
    uid = Column(Text, primary_key=True)
    callsign = Column(Text, nullable=True)
    iconsetpath = Column(Text, nullable=True)
    sipAddress = Column(Text, nullable=True)
    emailAddress = Column(Text, nullable=True)
    xmppUsername = Column(Text, nullable=True)
    endpoint = Column(Text, nullable=True)
    name = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)

    # relationships
    system_user = relationship('SystemUser', back_populates="contact")

    def __repr__(self) -> str:
        return super().__repr__() + f"uid={self.uid}, callsign={self.callsign}, iconsetpath={self.iconsetpath}, sipAddress={self.sipAddress}, emailAddress={self.emailAddress}, xmppUsername={self.xmppUsername}, endpoint={self.endpoint}, name={self.name}, phone={self.phone}"