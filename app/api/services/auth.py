from typing import Union

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.dependencies import get_db
from app.models.user import User as UserModel
from app.repositories.user import user_repo
from app.schemas.user import User as UserSchema, UserRegistrarse, UserCreate
from app.utils.encryptor import ActivationTokenEncoder


class AuthService:

    def __init__(self, db: Session = Depends(get_db)):
        self._db = db
        self._token_encoder = ActivationTokenEncoder(key=settings.authjwt_secret_key)

    def register_user(self, user: UserRegistrarse) -> UserModel:
        saved_user = user_repo.get_by_email(self._db, email=user.email)
        if saved_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists'
            )

        creat_user_dto = UserCreate(**user.dict(exclude_unset=True))
        return user_repo.create(self._db, dto_schema=creat_user_dto)

    def send_activation_email(self, activation_url: str, user: Union[UserModel, UserSchema]) -> None:
        pass

    def encode_user_activation_token(self, user: UserModel) -> str:
        return self._token_encoder.encode_token(user.email)

    def decode_user_activation_token(self, token: str) -> str:
        user_data = self._token_encoder.decode_token(activation_token=token)
        return user_data
