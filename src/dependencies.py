from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.services.books import BookService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_book_service(session: SessionDep) -> BookService:
    return BookService(session)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]
