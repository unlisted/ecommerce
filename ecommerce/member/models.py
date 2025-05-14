from ecommerce.common.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, UniqueConstraint
from uuid import UUID
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from reservation.models import Reservation


class Member(Base):
    __tablename__ = "member"
    __table_args__ = (UniqueConstraint("member_id"), )
    member_id: Mapped[UUID] = mapped_column(
        nullable=False, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    accounts: Mapped[list["Account"]] = relationship(back_populates="member")


class Account(Base):
    __tablename__ = "account"
    __table_args__ = (UniqueConstraint("account_id"), )
    account_id: Mapped[UUID] = mapped_column(
        nullable=False, server_default=func.gen_random_uuid()
    )
    member_id: Mapped[UUID] = mapped_column(ForeignKey("member.member_id"))

    member: Mapped[Member] = relationship(back_populates="accounts")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="account")
