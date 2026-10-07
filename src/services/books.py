from typing import Any
from uuid import UUID

from src.exceptions import EntityNotFoundError
from src.mappers.books import BookDataMapper, ChapterDataMapper
from src.models.books import BookChapterModelOrm, BookModelOrm
from src.repositories.book import BookRepository
from src.schemas.books import (
    BookCreate,
    BookListResponse,
    BookPageCursor,
    BookResponse,
    BookUpdate,
    ChapterCreate,
    ChapterListResponse,
    ChapterPageCursor,
    ChapterResponse,
    ChapterUpdate,
)


class BookService:
    def __init__(
        self,
        repository: BookRepository,
        book_mapper: BookDataMapper,
        chapter_mapper: ChapterDataMapper,
    ) -> None:
        self.repository = repository
        self.book_mapper = book_mapper
        self.chapter_mapper = chapter_mapper

    async def create(self, data: BookCreate) -> BookResponse:
        orm_obj = self.book_mapper.to_orm(data)
        created_book = await self.repository.create(orm_obj)
        return self.book_mapper.to_schema(created_book)

    async def get_page(
        self,
        limit: int,
        cursor: BookPageCursor | None = None,
    ) -> BookListResponse:
        books = await self.repository.get_page(
            limit + 1,
            cursor_created_at=cursor.created_at if cursor is not None else None,
            cursor_id=cursor.id if cursor is not None else None,
        )
        page_books = books[:limit]
        next_cursor = (
            BookPageCursor(
                created_at=page_books[-1].created_at,
                id=page_books[-1].id,
            )
            if len(books) > limit and page_books
            else None
        )

        return BookListResponse(
            items=self.book_mapper.to_schema_list(page_books),
            next_cursor=next_cursor,
        )

    async def get_one(self, **filter_by: Any) -> BookResponse:
        book = await self._get_book_or_raise(**filter_by)
        return self.book_mapper.to_schema(book)

    async def update(
        self,
        data: BookUpdate,
        **filter_by: Any,
    ) -> BookResponse:
        book = await self._get_book_or_raise(**filter_by)
        values = data.model_dump(exclude_unset=True)
        updated_book = await self.repository.update(book, values)
        return self.book_mapper.to_schema(updated_book)

    async def delete(self, **filter_by: Any) -> None:
        book = await self._get_book_or_raise(**filter_by)
        await self.repository.delete(book)

    async def _get_book_or_raise(self, **filter_by: Any) -> BookModelOrm:
        book = await self.repository.get_one_or_none(**filter_by)
        if book is None:
            raise EntityNotFoundError("Book not found")

        return book

    async def create_chapter(
        self,
        book_id: UUID,
        data: ChapterCreate,
    ) -> ChapterResponse:
        await self._get_book_or_raise(id=book_id)
        orm_obj = self.chapter_mapper.to_orm(data)
        orm_obj.book_id = book_id
        created_chapter = await self.repository.create_chapter(orm_obj)
        return self.chapter_mapper.to_schema(created_chapter)

    async def get_chapter_page(
        self,
        book_id: UUID,
        limit: int,
        cursor: ChapterPageCursor | None = None,
    ) -> ChapterListResponse:
        await self._get_book_or_raise(id=book_id)
        chapters = await self.repository.get_chapter_page(
            book_id=book_id,
            limit=limit + 1,
            cursor_created_at=cursor.created_at if cursor is not None else None,
            cursor_id=cursor.id if cursor is not None else None,
        )
        page_chapters = chapters[:limit]
        next_cursor = (
            ChapterPageCursor(
                created_at=page_chapters[-1].created_at,
                id=page_chapters[-1].id,
            )
            if len(chapters) > limit and page_chapters
            else None
        )

        return ChapterListResponse(
            items=self.chapter_mapper.to_schema_list(page_chapters),
            next_cursor=next_cursor,
        )

    async def get_chapter(
        self,
        book_id: UUID,
        chapter_id: UUID,
    ) -> ChapterResponse:
        await self._get_book_or_raise(id=book_id)
        chapter = await self._get_chapter_or_raise(
            book_id=book_id,
            id=chapter_id,
        )
        return self.chapter_mapper.to_schema(chapter)

    async def update_chapter(
        self,
        book_id: UUID,
        chapter_id: UUID,
        data: ChapterUpdate,
    ) -> ChapterResponse:
        await self._get_book_or_raise(id=book_id)
        chapter = await self._get_chapter_or_raise(
            book_id=book_id,
            id=chapter_id,
        )
        values = data.model_dump(exclude_unset=True)
        updated_chapter = await self.repository.update_chapter(chapter, values)
        return self.chapter_mapper.to_schema(updated_chapter)

    async def delete_chapter(
        self,
        book_id: UUID,
        chapter_id: UUID,
    ) -> None:
        await self._get_book_or_raise(id=book_id)
        chapter = await self._get_chapter_or_raise(
            book_id=book_id,
            id=chapter_id,
        )
        await self.repository.delete_chapter(chapter)

    async def _get_chapter_or_raise(
        self,
        **filter_by: Any,
    ) -> BookChapterModelOrm:
        chapter = await self.repository.get_chapter_one_or_none(**filter_by)
        if chapter is None:
            raise EntityNotFoundError("Chapter not found")

        return chapter
