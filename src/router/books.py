from uuid import UUID

from fastapi import APIRouter

from src.db import get_session
from src.schemas.books import BookCreate, BookResponse, BookUpdate
from src.services.books import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookResponse)
async def create_book(data: BookCreate):
    async with get_session() as session:
        service = BookService(session)
        return await service.create(data)


@router.get("", response_model=list[BookResponse])
async def get_books():
    async with get_session() as session:
        service = BookService(session)
        return await service.get_all()


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID):
    async with get_session() as session:
        service = BookService(session)
        return await service.get_one(id=book_id)


@router.patch("/{book_id}", response_model=BookResponse)
async def patch_book(book_id: UUID, data: BookUpdate):
    async with get_session() as session:
        service = BookService(session)
        return await service.update(data, id=book_id)


@router.delete("/{book_id}")
async def delete_book(book_id: UUID):
    async with get_session() as session:
        service = BookService(session)
        await service.delete(id=book_id)
        return {"status": "ok"}