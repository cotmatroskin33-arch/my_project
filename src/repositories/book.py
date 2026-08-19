from typing import Any

from src.models.books import BookModelOrm
from src.repositories.base import BaseRepository


class BookRepository(BaseRepository[BookModelOrm]):
    model: type[BookModelOrm] = BookModelOrm

    async def get_all(self) -> list[BookModelOrm]:
        return await self.get_filtered(
            self.model.is_deleted.is_(False)
        )

    async def delete(self, orm_obj: BookModelOrm) -> None:
        orm_obj.is_deleted = True
        await self.session.flush()

    async def get_one_or_none(self, **filter_by: Any) -> BookModelOrm | None:
        return await super().get_one_or_none(
            is_deleted=False,
            **filter_by,
        )
