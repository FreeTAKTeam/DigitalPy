from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .FilmologyManagement_base import FilmologyManagementBase

if TYPE_CHECKING:
    pass

class Genre(FilmologyManagementBase):
    """ 
    """

    __tablename__ = 'Genre'
    oid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]


