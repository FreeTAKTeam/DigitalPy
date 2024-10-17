from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from ...telemetry.persistence.TelemetryManagement_base import TelemetryManagementBase

if TYPE_CHECKING:
    pass

class SystemLog(TelemetryManagementBase):
    """ 
    """

    __tablename__ = 'SystemLog'
    oid: Mapped[str] = mapped_column(primary_key=True)
    severity: Mapped[str]
    file: Mapped[str]
    name: Mapped[str]
    message: Mapped[str]
    Name: Mapped[float]
    timestamp: Mapped[str]


