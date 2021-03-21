from typing import Any

from fastapi import APIRouter, Request
from fastapi.params import Depends, Path, Body
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from app.api.services.auth import AuthService
from app.dependencies.auth import get_authorized_user
from app.entities.user import User
from app.models.tokens import Tokens
from app.models.user import UserRegistrarse

router = APIRouter(
    tags=['auth']
)


@router.post('/registration')
async def registration(
        request: Request,
        background_tasks: BackgroundTasks,
        user: UserRegistrarse = Body(...),
        auth_service: AuthService = Depends(),
) -> Any:
    not_active_new_user = auth_service.register_user(user)

    activation_token = auth_service.encode_activation_token(user_data=user)
    activation_url = request.url_for('user_activation', activate_token=activation_token)

    background_tasks.add_task(
        auth_service.send_activation_email,
        activation_url=activation_url,
        user=not_active_new_user
    )
    return JSONResponse(status_code=HTTP_200_OK, content='success')


@router.get('/user_activation/{activate_token}')
async def user_activation(
        activate_token: str = Path(...),
        auth_service: AuthService = Depends(),
) -> Any:
    user_data = auth_service.decode_activation_token(token=activate_token)
    auth_service.activate_user_by_token(user_data)


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
