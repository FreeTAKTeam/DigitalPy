from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .component_management_base import Component_ManagementBase

if TYPE_CHECKING:
    pass

class Component(Component_ManagementBase):
    """ 
    """

    __tablename__ = 'Component'
    oid: Mapped[str] = mapped_column(primary_key=True)
    import_root: Mapped[str]
    installation_path: Mapped[str]
    author: Mapped[str]
    author_email: Mapped[str]
    description: Mapped[str]
    License: Mapped[str]
    repo: Mapped[str]
    requiredAlfaVersion: Mapped[str]
    URL: Mapped[str]
    Version: Mapped[str]
    UUID: Mapped[str]
    name: Mapped[str]


