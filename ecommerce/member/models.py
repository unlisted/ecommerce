from ecommerce.common.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey
from uuid import UUID


class Member(Base):
    __tablename__ = "member"
    member_id: Mapped[UUID] = mapped_column(
        nullable=False, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    accounts: Mapped[list["Account"]] = relationship(back_populates="member")


class Account(Base):
    __tablename__ = "account"
    account_id: Mapped[UUID] = mapped_column(
        nullable=False, server_default=func.gen_random_uuid()
    )
    member_id: Mapped[UUID] = mapped_column(ForeignKey("member.id"))

    member: Mapped[Member] = relationship(back_populates="accounts")
