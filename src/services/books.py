from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import EntityNotFoundError
from src.mappers.books import BookDataMapper
from src.models.books import BookModelOrm
from src.repositories.book import BookRepository
from src.schemas.books import BookCreate, BookResponse, BookUpdate


class BookService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = BookRepository(session)
        self.mapper = BookDataMapper()

    async def create(self, data: BookCreate) -> BookResponse:
        orm_obj = self.mapper.to_orm(data)
        created_book = await self.repository.create(orm_obj)
        await self.session.commit()
        return self.mapper.to_schema(created_book)

    async def get_all(self) -> list[BookResponse]:
        books = await self.repository.get_all()
        return self.mapper.to_schema_list(books)

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
        await self.session.commit()
        return self.mapper.to_schema(updated_book)

    async def delete(self, **filter_by: Any) -> None:
        book = await self._get_book_or_raise(**filter_by)
        await self.repository.delete(book)
        await self.session.commit()

    async def _get_book_or_raise(self, **filter_by: Any) -> BookModelOrm:
        book = await self.repository.get_one_or_none(**filter_by)
        if book is None:
            raise EntityNotFoundError("Book not found")

        return book
