from fastapi import HTTPException, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.db import get_db
from app.entities.user import User
from app.repositories.user import user_repo
from app.models.auth import AuthData
from app.utils import password_utils


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