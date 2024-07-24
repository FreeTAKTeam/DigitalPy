from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .component_management_base import Component_managementBase

if TYPE_CHECKING:
    from .component import Component

class ActionKey(Component_managementBase):
    """ 
    """

    __tablename__ = 'ActionKey'
    oid: Mapped[str] = mapped_column(primary_key=True)
    action: Mapped[str]
    context: Mapped[str]
    decorator: Mapped[str]
    config: Mapped[str]
    target: Mapped[str]
    source: Mapped[str]
    referencedBehaviour: Mapped[str]
    name: Mapped[str]

    Component_oid: Mapped[Optional[str]] = mapped_column(ForeignKey("Component.oid"))

