from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.book import BookRepository
from src.schemas.books import BookCreate, BookResponse, BookUpdate


class BookService:
    def __init__(self, session: AsyncSession):
        self.repository = BookRepository(session)

    async def create(self, data: BookCreate) -> BookResponse:
        return await self.repository.add(data)

    async def get_all(self) -> list[BookResponse]:
        return await self.repository.get_all()

    async def get_one(self, **filter_by) -> BookResponse:
        return await self.repository.get_one(**filter_by)

    async def update(
        self,
        data: BookUpdate,
        **filter_by,
    ) -> BookResponse:
        await self.repository.update(
            data,
            exclude_unset=True,
            **filter_by,
        )
        return await self.repository.get_one(**filter_by)

    async def delete(self, **filter_by) -> None:
        await self.repository.delete(**filter_by)