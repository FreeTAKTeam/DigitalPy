from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .FilmologyManagement_base import FilmologyManagementBase

if TYPE_CHECKING:
    pass

class EntityBaseExtended(FilmologyManagementBase):
    """ 
    """

    __tablename__ = 'EntityBaseExtended'
    oid: Mapped[str] = mapped_column(primary_key=True)
    creator: Mapped[str]
    created: Mapped[str]
    last_editor: Mapped[str]
    name: Mapped[str]
    description: Mapped[str]
    modified: Mapped[str]


