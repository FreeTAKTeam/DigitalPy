from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .FilmologyManagement_base import FilmologyManagementBase

if TYPE_CHECKING:
    from .movie import Movie

class Date(FilmologyManagementBase):
    """ 
    """

    __tablename__ = 'Date'
    oid: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[str]
    name: Mapped[str]

    DateAggregationMovie: Mapped[List["Movie"]] = relationship("Movie", lazy="joined")

    @validates('DateAggregationMovie_oid')
    def validate_DateAggregationMovie_oid(self, key, DateAggregationMovie_oid):
        if len(self.DateAggregationMovie) < 0:
            raise ValueError("Number of related instances from Date to DateAggregationMovie must be between 0 and -1.")
        return DateAggregationMovie_oid
