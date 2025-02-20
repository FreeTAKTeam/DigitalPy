# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

from typing import TYPE_CHECKING
# iterating associations
# found association
if TYPE_CHECKING:
    from .movie import Movie

class Date(Node):
    """"""
    def __init__(self, model_configuration, model, oid=None, node_type="Date") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._year: 'str' = None
        self._name: 'str' = None
        self._DateAggregationMovie: list[str] = []

    @property
    def year(self) -> 'str':
        """"""
        return self._year

    @year.setter
    def year(self, year: 'str'):
        year = str(year)
        if not isinstance(year, str):
            raise TypeError("'year' must be of type str")
        self._year= year

    @property
    def name(self) -> 'str':
        """"""
        return self._name

    @name.setter
    def name(self, name: 'str'):
        name = str(name)
        if not isinstance(name, str):
            raise TypeError("'name' must be of type str")
        self._name= name

    @property
    def DateAggregationMovie(self) -> list['str']: # type: ignore
        """"""
        return self._DateAggregationMovie

    @DateAggregationMovie.setter
    def DateAggregationMovie(self, DateAggregationMovie: 'str'):
        self._DateAggregationMovie = DateAggregationMovie
