from typing import Union

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.backgroud.tasks import send_html_email
from app.dependencies.db import get_db
from app.entities.user import User as UserEntity
from app.models.user import User as UserModel, UserRegistrarse, UserCreate, User
from app.repositories.user import user_repo
from app.utils.token_handler import TokenHandler


class AuthService:
    _ACTIVATION_EMAIL_SUBJECT = 'Postogramm Account Activation'
    _ACTIVATION_HTML_TEMPLATE = '''
    <html>
        <body>
               <div>
                Hi, <strong>{user_name}</strong>! 
                <br>
                <a href="{activation_link}"> Please, click here to activate your Postogramm account </>  
            </div> 
        </body>
    </html>
    '''

    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    def register_user(self, user: UserRegistrarse) -> UserEntity:
        saved_user = user_repo.get_by_email(self._db, email=user.email)
        if saved_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists'
            )

        creat_user_dto = UserCreate(**user.dict(exclude_unset=True))
        return user_repo.create(self._db, dto_schema=creat_user_dto)

    def send_activation_email(self, activation_url: str, user: Union[UserEntity, UserModel]) -> None:
        email_content = self._ACTIVATION_HTML_TEMPLATE.format(
            user_name=user.first_name,
            activation_link=activation_url
        )
        send_html_email(
            to=user.email,
            subject=self._ACTIVATION_EMAIL_SUBJECT,
            html=email_content
        )

    def activate_user_by_token(self, user_data: User) -> UserEntity:
        user = user_repo.get_by_email(self._db, email=user_data.email)

        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already activated'
            )

        user.is_active = True
        self._db.commit()

        return user

    @staticmethod
    def decode_activation_token(token: str) -> User:
        decode_token = TokenHandler.decode_token(token)
        return User(**decode_token)

    @staticmethod
    def encode_activation_token(user_data: UserRegistrarse) -> str:
        include_fields = {
            'email'
        }
        required_data = user_data.dict(include=include_fields)
        return TokenHandler.encode_token(data=required_data)
