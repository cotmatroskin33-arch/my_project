from typing import Any
from uuid import UUID

from sqlalchemy import select

from src.models.books import BookModelOrm
from src.repositories.base import BaseRepository


class BookRepository(BaseRepository[BookModelOrm]):
    model: type[BookModelOrm] = BookModelOrm

    async def get_page(
        self,
        limit: int,
        cursor: UUID | None = None,
    ) -> list[BookModelOrm]:
        query = select(self.model).where(self.model.is_deleted.is_(False))

        if cursor is not None:
            query = query.where(self.model.id > cursor)

        query = query.order_by(self.model.id.asc()).limit(limit)
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
