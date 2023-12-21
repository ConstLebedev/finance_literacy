from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from db.models import AbstractBaseModel

ModelType = TypeVar("ModelType", bound=AbstractBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A tortoise model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, id: Any) -> Optional[ModelType]:
        return await self.model.filter(id=id).first()

    async def get_multi(
        self, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return await self.model.all().offset(offset).limit(limit)

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = await self.model.create(**obj_in_data)
        return db_obj

    async def update(
        self,
        *,
        id: Any,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        queryset = self.model.filter(id=id)
        await queryset.update(**update_data)
        return await queryset.first()

    async def remove(self, *, id: int) -> ModelType:
        queryset = self.model.filter(id=id)
        removed = await queryset.first()
        await queryset.delete()
        return removed
