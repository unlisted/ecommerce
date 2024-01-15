from sqlalchemy import func, DateTime, create_engine
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker
from uuid import UUID
import os

DATABASE_URL = f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@postgres:5432/{os.getenv("POSTGRES_DB")}"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=func.gen_random_uuid()
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
