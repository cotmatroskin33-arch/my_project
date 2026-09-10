from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import and_, or_, select

from src.models.books import BookModelOrm
from src.repositories.base import BaseRepository


class BookRepository(BaseRepository[BookModelOrm]):
    model: type[BookModelOrm] = BookModelOrm

    async def get_page(
        self,
        limit: int,
        cursor_created_at: datetime | None = None,
        cursor_id: UUID | None = None,
    ) -> list[BookModelOrm]:
        query = select(self.model).where(self.model.is_deleted.is_(False))

        if cursor_created_at is not None and cursor_id is not None:
            query = query.where(
                or_(
                    self.model.created_at > cursor_created_at,
                    and_(
                        self.model.created_at == cursor_created_at,
                        self.model.id > cursor_id,
                    ),
                )
            )

        query = query.order_by(
            self.model.created_at.asc(),
            self.model.id.asc(),
        ).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def delete(self, orm_obj: BookModelOrm) -> None:
        orm_obj.is_deleted = True
        await self.session.flush()

    async def get_one_or_none(self, **filter_by: Any) -> BookModelOrm | None:
        return await super().get_one_or_none(
            is_deleted=False,
            **filter_by,
        )
