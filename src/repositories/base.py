from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


class   BaseRepository:
    model = None
    schema = None
    mapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: BaseModel):
        orm_obj = self.mapper.to_orm(data)
        self.session.add(orm_obj)
        await self.session.flush()
        return self.mapper.to_schema(orm_obj)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        await self.get_one_rec(**filter_by)  # проверяем существование

        update_stm = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stm)

    async def delete(self,**filter_by):
        await self.get_one_rec(**filter_by)
        update_stm = (
            update(self.model)
            .filter_by(**filter_by)
            .values(is_deleted=True)
        )
        await self.session.execute(update_stm)

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        # Здесь мы получаем ORM-объекты и преобразуем их в Pydantic
        orm_list = result.scalars().all()
        return self.mapper.to_schema_list(orm_list)

    async def get_all(self, **kwargs):
        return await self.get_filtered(**kwargs)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        orm_obj = result.scalars().one_or_none()
        if orm_obj is None:
            return None
        return self.mapper.to_schema(orm_obj)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            orm_obj = result.scalars().one()
            return self.mapper.to_schema(orm_obj)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Record not found")



    async def get_one_rec(self, **filter_by):
        """Возвращает ORM-объект (не схему) — нужен только для проверок"""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            return result.scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Record not found")
        except MultipleResultsFound:
            raise HTTPException(status_code=400, detail="Multiple objects found")

