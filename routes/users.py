from typing import List, Any, Optional, Tuple, Union
from fastapi import APIRouter, Depends, HTTPException
from tortoise.transactions import in_transaction

import crud
from db import models
import schemas
import depends
from security import get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.get("/", response_model=List[schemas.UserPydantic])
async def read_users(
        *,
        offset: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(depends.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = await crud.user.get_multi(offset=offset, limit=limit)
    return users


@router.post("/", response_model=schemas.UserPydantic)
async def create_user(
        *,
        user_in: schemas.UserCreatePydantic,
        email_in: schemas.EmailCreatePydantic,
        current_user: models.User = Depends(depends.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await crud.email.get_user(email=email_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    async with in_transaction():
        user_in = user_in.dict()
        if user_in.get('password'):
            user_in['password_hash'] = get_password_hash(user_in.get('password'))
        user = await crud.user.create(obj_in=user_in)
        email_in.user_id = user.id
        email = await crud.email.create(obj_in=email_in)
        return user


@router.get("/me",
            response_model=schemas.FullUserPydantic)
async def read_user_me(
        current_user: models.User = Depends(depends.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    email = await current_user.emails.filter(is_prime=True).first()
    return schemas.FullUserPydantic(user=current_user, email=email)


@router.post("/open", response_model=schemas.UserPydantic)
async def create_user_open(
        *,
        user_in: schemas.UserCreatePydantic,
        email_in: schemas.EmailCreatePydantic,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await crud.email.get_user(email=email_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    async with in_transaction():
        user_in = user_in.dict()
        if user_in.get('password'):
            user_in['password_hash'] = get_password_hash(user_in.get('password'))
        user = await crud.user.create(obj_in=user_in)
        email_in.user_id = user.id
        email = await crud.email.create(obj_in=email_in)
        return user
