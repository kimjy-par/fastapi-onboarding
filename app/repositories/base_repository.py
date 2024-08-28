from contextlib import AbstractAsyncContextManager
from typing import Callable, Type, TypeVar

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from pydantic import BaseModel

from app.core.exceptions import NotFoundError
from app.models.base_model import BaseModel


T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]], model: Type[T]):
        self.session_factory = session_factory
        self.model = model

    async def read_by_id(self, id: int, eager: bool = False) -> T:
        async with self.session_factory() as session:
            query = select(self.model).filter(self.model.id==id)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))

            result = await session.execute(query)
            result = result.scalars().first()
            if not result:
                raise NotFoundError
            
            return result
        
        
    async def create(self, schema: BaseModel) -> T:
        async with self.session_factory() as session:
            model = self.model(**schema.model_dump())
            session.add(model)
            await session.commit()
            await session.refresh(model)

            return model