import ecommerce.member.models #noqa
from sqlalchemy import func, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from enum import Enum
from typing import TYPE_CHECKING
from ecommerce.common.db import Base

if TYPE_CHECKING:
    from ecommerce.inventory.models import Item
    from ecommerce.member.models import Account


class ReservationStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"
    TIMED_OUT = "timed_out"


class Reservation(Base):
    __tablename__ = "reservation"

    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id"))
    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.account_id"))
    instance_id: Mapped[UUID] = mapped_column(
        nullable=False, server_default=func.gen_random_uuid()
    )
    status: Mapped[ReservationStatus] = mapped_column(
        "status", Text, nullable=False, default="active"
    )

    item: Mapped["Item"] = relationship("Item", back_populates="reservations")
    account: Mapped["Account"] = relationship("Account", back_populates="reservations")
