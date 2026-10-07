from datetime import datetime
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from src.dependencies import ReadBookServiceDep, WriteBookServiceDep
from src.schemas.books import (
    BookCreate,
    BookDeleteResponse,
    BookListResponse,
    BookPageCursor,
    BookResponse,
    BookUpdate,
    ChapterCreate,
    ChapterDeleteResponse,
    ChapterListResponse,
    ChapterPageCursor,
    ChapterResponse,
    ChapterUpdate,
)

router = APIRouter(prefix="/books", tags=["books"])


def _build_page_cursor(
    cursor_created_at: datetime | None,
    cursor_id: UUID | None,
    cursor_schema: type[BookPageCursor] | type[ChapterPageCursor],
) -> BookPageCursor | ChapterPageCursor | None:
    if cursor_created_at is None and cursor_id is None:
        return None

    if cursor_created_at is None or cursor_id is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="cursor_created_at and cursor_id must be provided together",
        )

    return cursor_schema(created_at=cursor_created_at, id=cursor_id)


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
    cursor_created_at: datetime | None = None,
    cursor_id: UUID | None = None,
) -> BookListResponse:
    cursor = _build_page_cursor(cursor_created_at, cursor_id, BookPageCursor)
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


@router.post("/{book_id}/chapters", response_model=ChapterResponse)
async def create_chapter(
    book_id: UUID,
    data: ChapterCreate,
    service: WriteBookServiceDep,
) -> ChapterResponse:
    return await service.create_chapter(book_id=book_id, data=data)


@router.get("/{book_id}/chapters", response_model=ChapterListResponse)
async def get_chapters(
    book_id: UUID,
    service: ReadBookServiceDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    cursor_created_at: datetime | None = None,
    cursor_id: UUID | None = None,
) -> ChapterListResponse:
    cursor = _build_page_cursor(cursor_created_at, cursor_id, ChapterPageCursor)
    return await service.get_chapter_page(
        book_id=book_id,
        limit=limit,
        cursor=cursor,
    )


@router.get("/{book_id}/chapters/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    book_id: UUID,
    chapter_id: UUID,
    service: ReadBookServiceDep,
) -> ChapterResponse:
    return await service.get_chapter(book_id=book_id, chapter_id=chapter_id)


@router.patch("/{book_id}/chapters/{chapter_id}", response_model=ChapterResponse)
async def patch_chapter(
    book_id: UUID,
    chapter_id: UUID,
    data: ChapterUpdate,
    service: WriteBookServiceDep,
) -> ChapterResponse:
    return await service.update_chapter(
        book_id=book_id,
        chapter_id=chapter_id,
        data=data,
    )


@router.delete("/{book_id}/chapters/{chapter_id}", response_model=ChapterDeleteResponse)
async def delete_chapter(
    book_id: UUID,
    chapter_id: UUID,
    service: WriteBookServiceDep,
) -> ChapterDeleteResponse:
    await service.delete_chapter(book_id=book_id, chapter_id=chapter_id)
    return ChapterDeleteResponse(status=HTTPStatus.OK.phrase.lower())
