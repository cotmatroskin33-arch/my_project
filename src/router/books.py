from uuid import UUID

from fastapi import APIRouter

from src.dependencies import BookServiceDep
from src.schemas.books import (
    BookCreate,
    BookDeleteResponse,
    BookResponse,
    BookUpdate,
)

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookResponse)
async def create_book(
    data: BookCreate,
    service: BookServiceDep,
) -> BookResponse:
    return await service.create(data)


@router.get("", response_model=list[BookResponse])
async def get_books(service: BookServiceDep) -> list[BookResponse]:
    return await service.get_all()


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: UUID,
    service: BookServiceDep,
) -> BookResponse:
    return await service.get_one(id=book_id)


@router.patch("/{book_id}", response_model=BookResponse)
async def patch_book(
    book_id: UUID,
    data: BookUpdate,
    service: BookServiceDep,
) -> BookResponse:
    return await service.update(data, id=book_id)


@router.delete("/{book_id}", response_model=BookDeleteResponse)
async def delete_book(
    book_id: UUID,
    service: BookServiceDep,
) -> BookDeleteResponse:
    await service.delete(id=book_id)
    return BookDeleteResponse(status="ok")
