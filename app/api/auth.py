from typing import Any

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT

from app.dependencies import get_authorized_user
from app.models.user import User
from app.schemas.tokens import Tokens

router = APIRouter(
    tags=['auth']
)


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
