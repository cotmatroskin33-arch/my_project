from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    price: int


class BookResponse(BookCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
    price: int | None = None