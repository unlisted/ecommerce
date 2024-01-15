from sqlalchemy import func, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from typing import TYPE_CHECKING
from enum import Enum

from ecommerce.common.db import Base


if TYPE_CHECKING:
    from inventory.models import Item  # Import Item only for type checking


class ReservationStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"
    TIMED_OUT = "timed_out"


class Reservation(Base):
    __tablename__ = "reservation"

    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id"))
    instance_id: Mapped[UUID] = mapped_column(
        nullable=False, server_default=func.gen_random_uuid()
    )
    status: Mapped[ReservationStatus] = mapped_column(
        "status", Text, nullable=False, default="active"
    )

    item: Mapped["Item"] = relationship(back_populates="reservations")
