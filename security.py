from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

import schemas
from settings import JWT_SECRET_KEY, JWT_ALGORYTHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORYTHM)
    return encoded_jwt


def decode_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORYTHM])
        sub = payload.get("sub")
        if sub == 'email':
            email = payload.get('email')
            token_data = schemas.TokenData(email=email)
        elif sub == 'ya':
            ya_id = payload.get('ya_id')
            token_data = schemas.TokenData(ya_id=ya_id)
        elif sub == 'vk':
            vk_id = payload.get('vk_id')
            token_data = schemas.TokenData(vk_id=vk_id)
        else:
            raise credentials_exception
        return token_data
    except jwt.ExpiredSignatureError:
        credentials_exception.detail = 'Token has expired'
        raise credentials_exception
