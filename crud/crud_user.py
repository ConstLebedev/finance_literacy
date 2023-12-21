from typing import Optional, Any

from .crud_base import CRUDBase
from db.models import User
from schemas import UserCreatePydantic, UserUpdatePydantic, Token
from security import verify_password, decode_access_token


class CRUDUser(CRUDBase[User, UserCreatePydantic, UserUpdatePydantic]):
    async def get_by_ya_id(self, *, id: str) -> Optional[User]:
        return await self.model.get_or_none(ya_id=id)

    async def get_by_vk_id(self, *, id: str) -> Optional[User]:
        return await self.model.get_or_none(vk_id=id)

    async def get_by_credentials(self, email: str, password: str) -> Optional[User]:
        from . import email as crud_email
        user = await crud_email.get_user(email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def check_token(self, token_schema: Token) -> Optional:
        """Проверка токена пользователя"""
        email = decode_access_token(token_schema.access_token)['email']
        from . import email as crud_email
        user = await crud_email.get_user(email=email)
        return user if user else None

    def is_superuser(self, user):
        return user.is_superuser

    def is_active(self, user):
        return user.is_active