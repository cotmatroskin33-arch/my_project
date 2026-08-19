from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class BookModelOrm(Base):
    __tablename__: str = "books"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    title: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        sa.Text(),
        nullable=False,
    )

    price: Mapped[int] = mapped_column(
        sa.Integer(),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        onupdate=sa.func.now(),
        nullable=True,
    )

    is_deleted: Mapped[bool] = mapped_column(
        sa.Boolean(),
        default=False,
        server_default=sa.false(),
        nullable=False,
    )
