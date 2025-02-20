from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .FilmologyManagement_base import FilmologyManagementBase

if TYPE_CHECKING:
    from .movie import Movie

class Actor(FilmologyManagementBase):
    """ 
    """

    __tablename__ = 'Actor'
    oid: Mapped[str] = mapped_column(primary_key=True)
    creator: Mapped[str]
    nationality: Mapped[str]
    surname: Mapped[str]
    created: Mapped[str]
    last_editor: Mapped[str]
    name: Mapped[str]
    birth: Mapped[str]
    description: Mapped[str]
    modified: Mapped[str]

    Movie_oid: Mapped[Optional[str]] = mapped_column(ForeignKey("Movie.oid"))

