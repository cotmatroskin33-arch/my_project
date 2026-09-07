from typing import Annotated

from fastapi import Depends

from src.dependencies.db import ReadSessionDep, WriteSessionDep
from src.mappers.books import BookDataMapper
from src.repositories.book import BookRepository
from src.services.books import BookService


def get_book_mapper() -> BookDataMapper:
    return BookDataMapper()


BookMapperDep = Annotated[BookDataMapper, Depends(get_book_mapper)]


def get_read_book_repository(session: ReadSessionDep) -> BookRepository:
    return BookRepository(session)


def get_write_book_repository(session: WriteSessionDep) -> BookRepository:
    return BookRepository(session)


ReadBookRepositoryDep = Annotated[BookRepository, Depends(get_read_book_repository)]
WriteBookRepositoryDep = Annotated[BookRepository, Depends(get_write_book_repository)]


def get_read_book_service(
    repository: ReadBookRepositoryDep,
    mapper: BookMapperDep,
) -> BookService:
    return BookService(repository, mapper)


def get_write_book_service(
    repository: WriteBookRepositoryDep,
    mapper: BookMapperDep,
) -> BookService:
    return BookService(repository, mapper)


ReadBookServiceDep = Annotated[BookService, Depends(get_read_book_service)]
WriteBookServiceDep = Annotated[BookService, Depends(get_write_book_service)]
