from typing import Type, TypeVar, Generic, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)


class CRUDBase(Generic[ModelType]):

    def __init__(
        self,
        model: Type[ModelType],
    ):
        self.model = model

    async def create(
        self,
        obj_in: dict[str, Any],
        session: AsyncSession,
    ) -> ModelType:
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_multi(
        self,
        session: AsyncSession,
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()
