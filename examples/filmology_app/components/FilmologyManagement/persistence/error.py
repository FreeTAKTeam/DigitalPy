from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .FilmologyManagement_base import FilmologyManagementBase

if TYPE_CHECKING:
    pass

class Error(FilmologyManagementBase):
    """ "Error"
    """

    __tablename__ = 'Error'
    oid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]


