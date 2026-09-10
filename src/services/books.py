from typing import Any

from src.exceptions import EntityNotFoundError
from src.mappers.books import BookDataMapper
from src.models.books import BookModelOrm
from src.repositories.book import BookRepository
from src.schemas.books import (
    BookCreate,
    BookListResponse,
    BookPageCursor,
    BookResponse,
    BookUpdate,
)


class BookService:
    def __init__(
        self,
        repository: BookRepository,
        mapper: BookDataMapper,
    ) -> None:
        self.repository = repository
        self.mapper = mapper

    async def create(self, data: BookCreate) -> BookResponse:
        orm_obj = self.mapper.to_orm(data)
        created_book = await self.repository.create(orm_obj)
        return self.mapper.to_schema(created_book)

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
            items=self.mapper.to_schema_list(page_books),
            next_cursor=next_cursor,
        )

    async def get_one(self, **filter_by: Any) -> BookResponse:
        book = await self._get_book_or_raise(**filter_by)
        return self.mapper.to_schema(book)

    async def update(
        self,
        data: BookUpdate,
        **filter_by: Any,
    ) -> BookResponse:
        book = await self._get_book_or_raise(**filter_by)
        values = data.model_dump(exclude_unset=True)
        updated_book = await self.repository.update(book, values)
        return self.mapper.to_schema(updated_book)

    async def delete(self, **filter_by: Any) -> None:
        book = await self._get_book_or_raise(**filter_by)
        await self.repository.delete(book)

    async def _get_book_or_raise(self, **filter_by: Any) -> BookModelOrm:
        book = await self.repository.get_one_or_none(**filter_by)
        if book is None:
            raise EntityNotFoundError("Book not found")

        return book
