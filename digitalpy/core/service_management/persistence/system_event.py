from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from ...telemetry.persistence.TelemetryManagement_base import TelemetryManagementBase

if TYPE_CHECKING:
    pass

class SystemEvent(TelemetryManagementBase):
    """ 
    """

    __tablename__ = 'SystemEvent'
    oid: Mapped[str] = mapped_column(primary_key=True)
    eventID: Mapped[str]
    name: Mapped[str]
    source: Mapped[str]
    message: Mapped[str]


