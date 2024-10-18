from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .Files_base import FilesBase

if TYPE_CHECKING:
    pass

class File(FilesBase):
    """ 
    """

    __tablename__ = 'File'
    oid: Mapped[str] = mapped_column(primary_key=True)
    path: Mapped[str]
    permissions: Mapped[str]
    size: Mapped[float]
    name: Mapped[str]


