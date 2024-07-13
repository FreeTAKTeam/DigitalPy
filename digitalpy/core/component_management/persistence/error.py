from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .component_management_base import Component_ManagementBase

if TYPE_CHECKING:
    pass

class Error(Component_ManagementBase):
    """ "Error"
    """

    __tablename__ = 'Error'
    oid: Mapped[str] = mapped_column(primary_key=True)


