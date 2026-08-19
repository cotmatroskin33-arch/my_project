from src.mappers.base import DataMapper
from src.models.books import BookModelOrm
from src.schemas.books import BookResponse


class BookDataMapper(DataMapper[BookModelOrm, BookResponse]):
    db_model: type[BookModelOrm] = BookModelOrm
    schema: type[BookResponse] = BookResponse
