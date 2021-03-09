from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Path
from fastapi_jwt_auth.auth_jwt import AuthJWT
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.dependencies.db import get_db
from app.entities.user import User
from app.repositories.post import post_repo
from app.repositories.user import user_repo


def get_current_user(
        db: Session = Depends(get_db),
        authorize: AuthJWT = Depends()
) -> User:
    authorize.jwt_required()

    user_email = authorize.get_jwt_subject()
    user = user_repo.get_by_email(db, email=user_email)

    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def get_user_post_owner(
        post_id: int = Path(...),
        db: Session = Depends(get_db),
        current_active_user: User = Depends(get_current_active_user)
) -> User:
    post = post_repo.get_post_by_id_and_author(
        db,
        id=post_id,
        author=current_active_user
    )
    if not post:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='User does not have permission for this post'
        )
    return current_active_user


def get_user_comment_owner(
        comments: int = Path(...),
        db: Session = Depends(get_db),
        current_active_user: User = Depends(get_current_active_user)
) -> User:
    pass
