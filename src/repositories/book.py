from src.mappers.books import BooksDataMapper
from src.models.books import BookModelOrm
from src.repositories.base import BaseRepository
from src.schemas.books import BookResponse


class BookRepository(BaseRepository):
    model = BookModelOrm
    schema = BookResponse
    mapper = BooksDataMapper()

    async def get_all(self):
        return await self.get_filtered(
            self.model.is_deleted.is_(False)
        )

    async def get_one(self, **filter_by):
        return await super().get_one(
            is_deleted=False,
            **filter_by
        )

    async def get_one_rec(self, **filter_by):
        return await super().get_one_rec(
            is_deleted=False,
            **filter_by,
        )

