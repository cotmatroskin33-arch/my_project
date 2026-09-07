from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from src.dependencies import ReadBookServiceDep, WriteBookServiceDep
from src.schemas.books import (
    BookCreate,
    BookDeleteResponse,
    BookListResponse,
    BookResponse,
    BookUpdate,
)

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookResponse)
async def create_book(
    data: BookCreate,
    service: WriteBookServiceDep,
) -> BookResponse:
    return await service.create(data)


@router.get("", response_model=BookListResponse)
async def get_books(
    service: ReadBookServiceDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    cursor: UUID | None = None,
) -> BookListResponse:
    return await service.get_page(limit=limit, cursor=cursor)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: UUID,
    service: ReadBookServiceDep,
) -> BookResponse:
    return await service.get_one(id=book_id)


@router.patch("/{book_id}", response_model=BookResponse)
async def patch_book(
    book_id: UUID,
    data: BookUpdate,
    service: WriteBookServiceDep,
) -> BookResponse:
    return await service.update(data, id=book_id)


@router.delete("/{book_id}", response_model=BookDeleteResponse)
async def delete_book(
    book_id: UUID,
    service: WriteBookServiceDep,
) -> BookDeleteResponse:
    await service.delete(id=book_id)
    return BookDeleteResponse(status=HTTPStatus.OK.phrase.lower())
