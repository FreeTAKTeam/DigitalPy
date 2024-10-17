from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from ...telemetry.persistence.TelemetryManagement_base import TelemetryManagementBase

if TYPE_CHECKING:
    pass

class ServiceStatus(TelemetryManagementBase):
    """ 
    """

    __tablename__ = 'ServiceStatus'
    oid: Mapped[str] = mapped_column(primary_key=True)
    upTime: Mapped[float]
    lastError: Mapped[float]
    ServiceName: Mapped[str]
    ServiceStatus: Mapped[str]
    Port: Mapped[float]
    name: Mapped[str]
    ServiceStatusActual: Mapped[str]


