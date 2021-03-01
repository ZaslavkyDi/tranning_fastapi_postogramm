from typing import Any

from fastapi import APIRouter, Request
from fastapi.params import Depends, Path, Body
from fastapi_jwt_auth.auth_jwt import AuthJWT

from app.api.services.auth import AuthService
from app.dependencies import get_authorized_user
from app.models.user import User
from app.schemas.tokens import Tokens
from app.schemas.user import UserRegistrarse

router = APIRouter(
    tags=['auth']
)


@router.post('/registration', response_model=Tokens, response_model_exclude_unset=True)
async def registration(
        user: UserRegistrarse = Body(...),
        auth_service: AuthService = Depends(),
        authorize: AuthJWT = Depends(),
        request: Request = None
) -> Any:
    not_active_new_user = auth_service.register_user(user)

    activation_key = auth_service.encode_user_activation_token(user=not_active_new_user)
    activation_url = request.url_for('user_activation', activate_key=activation_key)
    auth_service.send_activation_email(
        activation_url=activation_url,
        user=not_active_new_user
    )
    return Tokens(
        access_token=authorize.create_access_token(subject=not_active_new_user.email, fresh=False),
    )


@router.get('/user_activation/{activate_key}')
async def user_activation(
        activate_key: str = Path(...),
        authorize: AuthJWT = Depends(),
) -> Any:
    # 1. get user from the token
    # 2. activate user
    # 3. redirect to login
    pass


@router.post('/login', response_model=Tokens)
async def login(
        authorized_user: User = Depends(get_authorized_user),
        authorize: AuthJWT = Depends(),
) -> Any:
    return Tokens(
        access_token=authorize.create_access_token(subject=authorized_user.email, fresh=True),
        refresh_token=authorize.create_refresh_token(subject=authorized_user.email),
    )


@router.post('/refresh', response_model=Tokens, response_model_exclude_unset=True, operation_id="authorize")
async def refresh_token(authorize: AuthJWT = Depends()) -> Any:
    authorize.jwt_refresh_token_required()
    user_email = authorize.get_jwt_subject()
    return Tokens(
        access_token=authorize.create_access_token(subject=user_email, fresh=True)
    )
