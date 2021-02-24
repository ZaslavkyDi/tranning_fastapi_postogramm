from typing import Generator

import fastapi
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic.error_wrappers import ValidationError

from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.user import user_repo


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        db: SessionLocal = Depends(get_db),
        authorize: AuthJWT = Depends()
) -> User:
    authorize.jwt_required()
    try:
        pass
    except (AuthJWTException, ValidationError):
        raise HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user_email = authorize.get_jwt_subject()
    user = user_repo.get_by_email(db, email=user_email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")

    return current_user
