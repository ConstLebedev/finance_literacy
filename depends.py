from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import crud
import schemas
from security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    token_data = decode_access_token(token)
    if token_data.email:
        usr = await crud.email.get_user(email=token_data.email)
    elif token_data.vk_id:
        usr = await crud.user.get_by_vk_id(id=token_data.vk_id)
    elif token_data.ya_id:
        usr = await crud.user.get_by_ya_id(id=token_data.ya_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad token data"
        )
    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usr


async def get_current_active_user(current_user: Annotated[schemas.UserPydantic, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: Annotated[schemas.UserPydantic, Depends(get_current_active_user)]):
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="not a superuser")
    return current_user
