from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import and_, or_, select

from src.models.books import BookChapterModelOrm, BookModelOrm
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

    async def create_chapter(
        self,
        orm_obj: BookChapterModelOrm,
    ) -> BookChapterModelOrm:
        self.session.add(orm_obj)
        await self.session.flush()
        await self.session.refresh(orm_obj)
        return orm_obj

    async def get_chapter_page(
        self,
        book_id: UUID,
        limit: int,
        cursor_created_at: datetime | None = None,
        cursor_id: UUID | None = None,
    ) -> list[BookChapterModelOrm]:
        query = select(BookChapterModelOrm).where(
            BookChapterModelOrm.book_id == book_id,
            BookChapterModelOrm.is_deleted.is_(False),
        )

        if cursor_created_at is not None and cursor_id is not None:
            query = query.where(
                or_(
                    BookChapterModelOrm.created_at > cursor_created_at,
                    and_(
                        BookChapterModelOrm.created_at == cursor_created_at,
                        BookChapterModelOrm.id > cursor_id,
                    ),
                )
            )

        query = query.order_by(
            BookChapterModelOrm.created_at.asc(),
            BookChapterModelOrm.id.asc(),
        ).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_chapter_one_or_none(
        self,
        **filter_by: Any,
    ) -> BookChapterModelOrm | None:
        query = select(BookChapterModelOrm).filter_by(
            is_deleted=False,
            **filter_by,
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def update_chapter(
        self,
        orm_obj: BookChapterModelOrm,
        values: dict[str, Any],
    ) -> BookChapterModelOrm:
        for field, value in values.items():
            setattr(orm_obj, field, value)

        await self.session.flush()
        await self.session.refresh(orm_obj)
        return orm_obj

    async def delete_chapter(self, orm_obj: BookChapterModelOrm) -> None:
        orm_obj.is_deleted = True
        await self.session.flush()
