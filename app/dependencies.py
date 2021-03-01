from typing import Generator

from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Body
from fastapi_jwt_auth.auth_jwt import AuthJWT
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.user import user_repo
from app.schemas.auth import AuthData
from app.utils import password_utils


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


def get_user_post_owner(current_active_user: User = Depends(get_current_active_user)) -> User:
    pass


def get_authorized_user(
        db: Session = Depends(get_db),
        auth_data: AuthData = Body(...)
) -> User:
    saved_user = user_repo.get_by_email(db, email=auth_data.email)
    if not saved_user:
        raise HTTPException(status_code=404, detail="User not found")

    is_verified = password_utils.verify_password(
        password=auth_data.password,
        hashed_password=saved_user.hashed_password
    )
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    return saved_user
