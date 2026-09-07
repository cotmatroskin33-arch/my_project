from fastapi import APIRouter

from src.router.books import router as books_router

router = APIRouter(prefix="/api/v1")
router.include_router(books_router)
