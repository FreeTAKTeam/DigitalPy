from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .component_management_base import Component_managementBase

if TYPE_CHECKING:
    from .actionkey import ActionKey

class Component(Component_managementBase):
    """ 
    """

    __tablename__ = 'Component'
    oid: Mapped[str] = mapped_column(primary_key=True)
    author: Mapped[str]
    author_email: Mapped[str]
    description: Mapped[str]
    License: Mapped[str]
    repo: Mapped[str]
    requiredAlfaVersion: Mapped[str]
    URL: Mapped[str]
    Version: Mapped[str]
    UUID: Mapped[str]
    isActive: Mapped[str]
    isInstalled: Mapped[str]
    installationPath: Mapped[str]
    name: Mapped[str]


