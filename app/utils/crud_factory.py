from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaModel = TypeVar("UpdateSchemaModel", bound=BaseModel)


class CrudFactory(Generic[ModelType, CreateSchemaType, UpdateSchemaModel]):
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model

    async def create(self, create_post: CreateSchemaType) -> ModelType:
        post = self.model(**create_post.model_dump())
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def getAll(self) -> List[ModelType]:
        results = await self.db.execute(select(self.model))
        return list(results.scalars().all())

    async def getById(self, id: int) -> ModelType | None:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def handle_update(self, id: int, post: UpdateSchemaModel) -> ModelType | None:
        stmt = (
            update(self.model)
            .where(getattr(self.model, "id") == id)
            .values(**post.model_dump())
            .returning(self.model)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def handle_delete(self, id: int) -> int:
        stmt = delete(self.model).where(getattr(self.model, "id") == id)
        result = await self.db.execute(stmt)

        return result.rowcount
