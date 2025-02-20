from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .FilmologyManagement_base import FilmologyManagementBase

if TYPE_CHECKING:
    pass

class Image(FilmologyManagementBase):
    """ 
    """

    __tablename__ = 'Image'
    oid: Mapped[str] = mapped_column(primary_key=True)
    fileName: Mapped[str]
    name: Mapped[str]


