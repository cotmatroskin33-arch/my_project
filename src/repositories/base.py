from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[ModelT]:
    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, orm_obj: ModelT) -> ModelT:
        self.session.add(orm_obj)
        await self.session.flush()
        await self.session.refresh(orm_obj)
        return orm_obj

    async def update(
        self,
        orm_obj: ModelT,
        values: dict[str, Any],
    ) -> ModelT:
        for field, value in values.items():
            setattr(orm_obj, field, value)

        await self.session.flush()
        await self.session.refresh(orm_obj)
        return orm_obj

    async def get_one_or_none(self, **filter_by: Any) -> ModelT | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
