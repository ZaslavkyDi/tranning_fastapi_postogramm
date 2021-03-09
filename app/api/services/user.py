from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.dependencies.db import get_db
from app.entities.user import User
from app.repositories.user import user_repo
from app.models.user import UserCreate, UserUpdate


class UserService:

    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    def get_users(self, skip: int, limit: int) -> List[User]:
        if limit == 0:
            users = user_repo.get_all(self._db)
        else:
            users = user_repo.get_multi(self._db, skip=skip, limit=limit)

        return users

    def get_user_by_id(self, user_id: int) -> User:
        return user_repo.get(self._db, id=user_id)

    def create_user(self, user_data: UserCreate) -> User:
        user = user_repo.get_by_email(self._db, email=user_data.email)
        if user:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail='User already exists'
            )
        return user_repo.create(self._db, dto_schema=user_data)

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        saved_user = user_repo.get(self._db, id=user_id)
        if not saved_user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user_repo.update(self._db, entity=saved_user, dto_schema=user_data)

    def delete_user(self, user_id: int) -> User:
        return user_repo.delete(self._db, id=user_id)
