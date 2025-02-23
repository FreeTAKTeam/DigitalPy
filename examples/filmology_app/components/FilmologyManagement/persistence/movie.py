from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .FilmologyManagement_base import FilmologyManagementBase

if TYPE_CHECKING:
    from .actor import Actor
    from .poster import Poster
    from .date import Date
    from .director import Director

class Movie(FilmologyManagementBase):
    """ 
    """

    __tablename__ = 'Movie'
    oid: Mapped[str] = mapped_column(primary_key=True)
    date: Mapped[str]
    country: Mapped[str]
    creator: Mapped[str]
    color: Mapped[str]
    created: Mapped[str]
    last_editor: Mapped[str]
    runtime: Mapped[str]
    description: Mapped[str]
    URL: Mapped[str]
    plot: Mapped[str]
    name: Mapped[str]
    alias: Mapped[str]
    modified: Mapped[str]

    CompositionPosterPrimary_oid: Mapped[str] = mapped_column(ForeignKey("Poster.oid"))
    CompositionPosterPrimary: Mapped["Poster"] = relationship("Poster", lazy="joined")
    Date_oid: Mapped[str] = mapped_column(ForeignKey("Date.oid"))
    Date: Mapped["Date"] = relationship("Date", lazy="joined")
    CompositionActor_oid: Mapped[Optional[str]] = mapped_column(ForeignKey("Actor.oid"))
    Director_oid: Mapped[Optional[str]] = mapped_column(ForeignKey("Director.oid"))

