from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .TelemetryManagement_base import TelemetryManagementBase

if TYPE_CHECKING:
    from .span import Span
    from .resource import Resource
    from .instrumentationlibrary import InstrumentationLibrary

class Trace(TelemetryManagementBase):
    """ 
    """

    __tablename__ = 'Trace'
    oid: Mapped[str] = mapped_column(primary_key=True)
    traceId: Mapped[float]
    name: Mapped[str]


