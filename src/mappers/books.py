from src.mappers.base import DataMapper
from src.models.books import BookChapterModelOrm, BookModelOrm
from src.schemas.books import BookResponse, ChapterResponse


class BookDataMapper(DataMapper[BookModelOrm, BookResponse]):
    db_model: type[BookModelOrm] = BookModelOrm
    schema: type[BookResponse] = BookResponse


class ChapterDataMapper(DataMapper[BookChapterModelOrm, ChapterResponse]):
    db_model: type[BookChapterModelOrm] = BookChapterModelOrm
    schema: type[ChapterResponse] = ChapterResponse
