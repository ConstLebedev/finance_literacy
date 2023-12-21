from typing import Optional

from .crud_base import CRUDBase
from db.models import User, Email
from schemas import EmailCreatePydantic, EmailUpdatePydantic


class CRUDEmail(CRUDBase[Email, EmailCreatePydantic, EmailUpdatePydantic]):
    async def get_user(self, *, email: str) -> Optional[User]:
        email = await Email.filter(email=email).first().prefetch_related('user')
        if email:
            return email.user

    async def get_by_user(self, *, user_id) -> Optional[User]:
        return await self.model.get_or_none(user_id=user_id)
