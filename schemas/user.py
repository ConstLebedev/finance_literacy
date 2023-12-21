from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from db import models

UserPydantic = pydantic_model_creator(
    models.User,
    name='UserPydantic'
)


class UserCreatePydantic(
    pydantic_model_creator(
        models.User,
        name='UserCreatePydantic',
        exclude=('id', 'vk_id', 'ya_id', 'created_at', 'modified_at',),
        optional=('password_hash',)
    )
):
    password: str


UserYandexCreatePydantic = pydantic_model_creator(
    models.User,
    name='UserYandexCreatePydantic',
    include=('username', 'ya_id', 'is_verify', 'is_active')
)

UserVkCreatePydantic = pydantic_model_creator(
    models.User,
    name='UserVkCreatePydantic',
    include=('username', 'vk_id', 'is_verify', 'is_active')
)


class UserUpdatePydantic(
    pydantic_model_creator(
        models.User,
        name='UserUpdatePydantic',
        exclude=('id', 'created_at', 'modified_at',),
        optional=('password_hash',)
    )
):
    password: str


EmailPydantic = pydantic_model_creator(
    models.Email,
    name='EmailPydantic'
)

EmailUpdatePydantic = pydantic_model_creator(
    models.Email,
    name='EmailUpdatePydantic',
    exclude=('id',)
)


class EmailCreatePydantic(
    pydantic_model_creator(
        models.Email,
        name='EmailCreatePydantic',
        exclude=('id',), )
):
    user_id: Optional[int] = None


class FullUserPydantic(BaseModel):
    user: UserPydantic
    email: EmailPydantic
