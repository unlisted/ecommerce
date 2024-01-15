from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from ecommerce.common.db import Base

from ecommerce.reservation.models import Reservation


class Item(Base):
    __tablename__ = "item"

    sku_number: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    unit_cost_cents: Mapped[int] = mapped_column(nullable=False)

    item_stock: Mapped["ItemStock"] = relationship(back_populates="item")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="item")


class ItemStock(Base):
    __tablename__ = "item_stock"

    quantity_available: Mapped[int] = mapped_column(nullable=False, default=0)

    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id"))
    item: Mapped[Item] = relationship(back_populates="item_stock")
