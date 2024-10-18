from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List, Optional

from .TelemetryManagement_base import TelemetryManagementBase

if TYPE_CHECKING:
    pass

class Metric(TelemetryManagementBase):
    """ 
    """

    __tablename__ = 'Metric'
    oid: Mapped[str] = mapped_column(primary_key=True)
    unit: Mapped[float]
    metricName: Mapped[str]
    valueExpected: Mapped[float]
    name: Mapped[str]
    description: Mapped[str]
    ID: Mapped[str]
    value: Mapped[float]
    timestamp: Mapped[str]


