from typing import Annotated
from datetime import timedelta

import httpx
from fastapi import Depends, Request, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from security import create_access_token
import crud
import schemas
from settings import JWT_EXPIRE_MINUTES, YANDEX_CLIENT_ID, YANDEX_CLIENT_SECRET, \
    YANDEX_TOKEN_URI, YANDEX_CODE_URI, VK_TOKEN_URI, VK_CODE_URI, VK_CLIENT_ID, VK_CLIENT_SECRET

router = APIRouter(prefix='/auth', tags=['auth'])
client = httpx.AsyncClient()


class PydanticOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    pass


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: Annotated[PydanticOAuth2PasswordRequestForm, Depends()]
):
    user = await crud.user.get_by_credentials(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email_obj = await user.emails.filter(is_prime=True).first()
    access_token = create_access_token(
        data={"sub": "email", "email": email_obj.email}, expires_delta=timedelta(minutes=JWT_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


@router.get("/login/yandex", response_model=None)
async def yandex_login(request: Request):
    params = dict(client_id=YANDEX_CLIENT_ID,
                  response_type='code',
                  redirect_uri=str(request.url_for(yandex_token.__name__)),
                  force_confirm='yes')
    url = f'{YANDEX_CODE_URI}/?{"&".join("=".join(pair) for pair in params.items())}'
    return url


@router.get("/token/yandex", response_model=schemas.Token)
async def yandex_token(request: Request):
    response = await client.post(YANDEX_TOKEN_URI, data={'grant_type': 'authorization_code',
                                                         'code': request.query_params['code'],
                                                         'client_id': YANDEX_CLIENT_ID,
                                                         'client_secret': YANDEX_CLIENT_SECRET})
    ya_access_token = response.json()['access_token']
    response = await client.get('https://login.yandex.ru/info',
                                headers={'Authorization': 'OAuth ' + ya_access_token})
    user_info = response.json()
    user = await crud.user.get_by_ya_id(id=user_info['id'])
    if not user:
        user_schema = schemas.UserYandexCreatePydantic(
            username=user_info['default_email'],
            ya_id=user_info['id'],
            is_verify=True,
            is_active=True
        )
        user = await crud.user.create(obj_in=user_schema)
        email_schema = schemas.EmailCreatePydantic(
            email=user_info['default_email'],
            is_prime=True,
            user_id=user.id
        )
        email = await crud.email.create(obj_in=email_schema)
    access_token = create_access_token(
        data={"sub": "ya", "ya_id": user.ya_id}, expires_delta=timedelta(minutes=JWT_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/login/vk", response_model=None)
async def vk_login(request: Request):
    params = dict(client_id=VK_CLIENT_ID,
                  redirect_uri=str(request.url_for(vk_token.__name__)),
                  scope=str(4194304 + 268435456))  # email + phone # https://dev.vk.com/ru/reference/access-rights
    url = f'{VK_CODE_URI}/?{"&".join("=".join(pair) for pair in params.items())}'
    return url


@router.get("/token/vk", response_model=schemas.Token)
async def vk_token(request: Request):
    response = await client.get(VK_TOKEN_URI,
                                params={'client_id': VK_CLIENT_ID,
                                        'client_secret': VK_CLIENT_SECRET,
                                        'redirect_uri': str(request.url_for(vk_token.__name__)),
                                        'code': request.query_params['code']})
    user_info = response.json()
    # vk_access_token = user_info['access_token']  # если нужно получать дополнительную инфу о пользователе
    user = await crud.user.get_by_vk_id(id=user_info['user_id'])
    if not user:
        user_schema = schemas.UserVkCreatePydantic(
            username=user_info['email'],
            vk_id=str(user_info['user_id']),
            is_verify=True,
            is_active=True
        )
        user = await crud.user.create(obj_in=user_schema)
        email_schema = schemas.EmailCreatePydantic(
            email=user_info['email'],
            is_prime=True,
            user_id=user.id
        )
        email = await crud.email.create(obj_in=email_schema)
    access_token = create_access_token(
        data={"sub": "vk", "vk_id":  user.vk_id}, expires_delta=timedelta(minutes=JWT_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
