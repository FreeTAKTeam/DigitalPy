# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

from typing import TYPE_CHECKING
# iterating associations
# found association
if TYPE_CHECKING:
    from .movie import Movie
# found association
if TYPE_CHECKING:
    from .poster import Poster
# found association
if TYPE_CHECKING:
    from .date import Date

class Movie(Node):
    """"""
    def __init__(self, model_configuration, model, oid=None, node_type="Movie") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._date: 'str' = None
        self._country: 'str' = None
        self._Movie: list[str] = []
        self._creator: 'str' = None
        self._color: 'str' = None
        self._created: 'str' = None
        self._last_editor: 'str' = None
        self._runtime: 'str' = None
        self._description: 'str' = None
        self._URL: 'str' = None
        self._CompositionPosterPrimary: str = ""
        self._Date: str = ""
        self._plot: 'str' = None
        self._name: 'str' = None
        self._alias: 'str' = None
        self._modified: 'str' = None

    @property
    def date(self) -> 'str':
        """"""
        return self._date

    @date.setter
    def date(self, date: 'str'):
        date = str(date)
        if not isinstance(date, str):
            raise TypeError("'date' must be of type str")
        self._date= date

    @property
    def country(self) -> 'str':
        """"""
        return self._country

    @country.setter
    def country(self, country: 'str'):
        country = str(country)
        if not isinstance(country, str):
            raise TypeError("'country' must be of type str")
        self._country= country

    @property
    def creator(self) -> 'str':
        """user name of the creator"""
        return self._creator

    @creator.setter
    def creator(self, creator: 'str'):
        creator = str(creator)
        if not isinstance(creator, str):
            raise TypeError("'creator' must be of type str")
        self._creator= creator

    @property
    def color(self) -> 'str':
        """"""
        return self._color

    @color.setter
    def color(self, color: 'str'):
        color = str(color)
        if not isinstance(color, str):
            raise TypeError("'color' must be of type str")
        self._color= color

    @property
    def created(self) -> 'str':
        """"""
        return self._created

    @created.setter
    def created(self, created: 'str'):
        created = str(created)
        if not isinstance(created, str):
            raise TypeError("'created' must be of type str")
        self._created= created

    @property
    def last_editor(self) -> 'str':
        """"""
        return self._last_editor

    @last_editor.setter
    def last_editor(self, last_editor: 'str'):
        last_editor = str(last_editor)
        if not isinstance(last_editor, str):
            raise TypeError("'last_editor' must be of type str")
        self._last_editor= last_editor

    @property
    def runtime(self) -> 'str':
        """"""
        return self._runtime

    @runtime.setter
    def runtime(self, runtime: 'str'):
        runtime = str(runtime)
        if not isinstance(runtime, str):
            raise TypeError("'runtime' must be of type str")
        self._runtime= runtime

    @property
    def description(self) -> 'str':
        """"""
        return self._description

    @description.setter
    def description(self, description: 'str'):
        description = str(description)
        if not isinstance(description, str):
            raise TypeError("'description' must be of type str")
        self._description= description

    @property
    def URL(self) -> 'str':
        """"""
        return self._URL

    @URL.setter
    def URL(self, URL: 'str'):
        URL = str(URL)
        if not isinstance(URL, str):
            raise TypeError("'URL' must be of type str")
        self._URL= URL

    @property
    def plot(self) -> 'str':
        """"""
        return self._plot

    @plot.setter
    def plot(self, plot: 'str'):
        plot = str(plot)
        if not isinstance(plot, str):
            raise TypeError("'plot' must be of type str")
        self._plot= plot

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
    def alias(self) -> 'str':
        """"""
        return self._alias

    @alias.setter
    def alias(self, alias: 'str'):
        alias = str(alias)
        if not isinstance(alias, str):
            raise TypeError("'alias' must be of type str")
        self._alias= alias

    @property
    def modified(self) -> 'str':
        """"""
        return self._modified

    @modified.setter
    def modified(self, modified: 'str'):
        modified = str(modified)
        if not isinstance(modified, str):
            raise TypeError("'modified' must be of type str")
        self._modified= modified

    @property
    def CompositionPosterPrimary(self) -> 'str': # type: ignore
        """"""
        return self._CompositionPosterPrimary

    @CompositionPosterPrimary.setter
    def CompositionPosterPrimary(self, CompositionPosterPrimary: 'str'):
        self._CompositionPosterPrimary = CompositionPosterPrimary

    @property
    def Date(self) -> 'str': # type: ignore
        """"""
        return self._Date

    @Date.setter
    def Date(self, Date: 'str'):
        self._Date = Date
