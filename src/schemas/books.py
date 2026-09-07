from datetime import datetime
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator
from pydantic_core import PydanticCustomError

BookTitle = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=255),
]
BookAuthor = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=255),
]
BookDescription = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]
BookPrice = Annotated[int, Field(gt=0)]


class BookCreate(BaseModel):
    title: BookTitle
    author: BookAuthor
    description: BookDescription
    price: BookPrice


class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    description: str
    price: int
    created_at: datetime
    updated_at: datetime | None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class BookListResponse(BaseModel):
    items: list[BookResponse]
    next_cursor: UUID | None = None


class BookUpdate(BaseModel):
    title: BookTitle | None = None
    author: BookAuthor | None = None
    description: BookDescription | None = None
    price: BookPrice | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> Self:
        if not self.model_fields_set:
            raise PydanticCustomError(
                "empty_update_payload",
                "At least one field must be provided",
            )

        none_fields = [
            field for field in self.model_fields_set if getattr(self, field) is None
        ]
        if none_fields:
            raise PydanticCustomError(
                "null_update_field",
                "Fields cannot be null: {fields}",
                {"fields": ", ".join(none_fields)},
            )

        return self


class BookDeleteResponse(BaseModel):
    status: Literal["ok"]
