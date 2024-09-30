from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .TelemetryManagement_base import TelemetryManagementBase

if TYPE_CHECKING:
    from .trace import Trace

class Span(TelemetryManagementBase):
    """ 
    """

    __tablename__ = 'Span'
    oid: Mapped[str] = mapped_column(primary_key=True)
    spanId: Mapped[float]
    traceId: Mapped[float]
    relatedSpanID: Mapped[str]
    kind: Mapped[str]
    name: Mapped[str]
    startTime: Mapped[str]
    endTime: Mapped[str]

    Trace_oid: Mapped[Optional[str]] = mapped_column(ForeignKey("Trace.oid"))

