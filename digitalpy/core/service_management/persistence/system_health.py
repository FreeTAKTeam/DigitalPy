from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from ...telemetry.persistence.TelemetryManagement_base import TelemetryManagementBase

if TYPE_CHECKING:
    pass

class SystemHealth(TelemetryManagementBase):
    """ 
    """

    __tablename__ = 'SystemHealth'
    oid: Mapped[str] = mapped_column(primary_key=True)
    disk: Mapped[float]
    memory: Mapped[float]
    name: Mapped[str]
    cpu: Mapped[float]
    timestamp: Mapped[str]


