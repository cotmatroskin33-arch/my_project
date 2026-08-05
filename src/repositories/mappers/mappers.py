from src.models.books import BookModelOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.books import BookResponse


class BooksDataMapper(DataMapper):
    db_model = BookModelOrm
    schema = BookResponse