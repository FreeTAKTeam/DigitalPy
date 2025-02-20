# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

from typing import TYPE_CHECKING
# iterating associations
# found association
if TYPE_CHECKING:
    from .actor import Actor

class Actor(Node):
    """"""
    def __init__(self, model_configuration, model, oid=None, node_type="Actor") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._creator: 'str' = None
        self._nationality: 'str' = None
        self._surname: 'str' = None
        self._created: 'str' = None
        self._Actor: list[str] = []
        self._last_editor: 'str' = None
        self._name: 'str' = None
        self._birth: 'str' = None
        self._description: 'str' = None
        self._modified: 'str' = None

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
    def nationality(self) -> 'str':
        """"""
        return self._nationality

    @nationality.setter
    def nationality(self, nationality: 'str'):
        nationality = str(nationality)
        if not isinstance(nationality, str):
            raise TypeError("'nationality' must be of type str")
        self._nationality= nationality

    @property
    def surname(self) -> 'str':
        """"""
        return self._surname

    @surname.setter
    def surname(self, surname: 'str'):
        surname = str(surname)
        if not isinstance(surname, str):
            raise TypeError("'surname' must be of type str")
        self._surname= surname

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
    def birth(self) -> 'str':
        """"""
        return self._birth

    @birth.setter
    def birth(self, birth: 'str'):
        birth = str(birth)
        if not isinstance(birth, str):
            raise TypeError("'birth' must be of type str")
        self._birth= birth

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
    def modified(self) -> 'str':
        """"""
        return self._modified

    @modified.setter
    def modified(self, modified: 'str'):
        modified = str(modified)
        if not isinstance(modified, str):
            raise TypeError("'modified' must be of type str")
        self._modified= modified
