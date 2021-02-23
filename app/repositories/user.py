from typing import Optional, Union, Dict, Any

from sqlalchemy.orm.session import Session

from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate
from app.utils.passwrod import BCryptPasswordUtils


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):

    def __init__(self):
        super(UserRepository, self).__init__(model_type=User)
        self.password_utils = BCryptPasswordUtils()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model_type).filter(self.model_type.email == email).first()

    def create(self, db: Session, *, dto_schema: UserCreate) -> User:
        hashed_password = self.password_utils.encrypt_password(dto_schema.password)
        dto_data = dto_schema.dict()
        del dto_data['password']

        entity = User(
            **dto_data,
            hashed_password=hashed_password
        )
        db.add(entity)
        db.commit()
        db.refresh(entity)

        return entity

    def update(
            self, db: Session, *,
            entity: User,
            dto_schema: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(dto_schema, Dict):
            update_data = dto_schema
        else:
            update_data = dto_schema.dict(exclude_unset=True)

        new_password = update_data['password']
        if new_password:
            hashed_password = self.password_utils.encrypt_password(new_password)
            update_data['hashed_password'] = hashed_password
            del update_data['password']

        return super().update(db, entity=entity, dto_schema=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)

        if not user or not self.password_utils.verify_password(password, hashed_password=user.hashed_password):
            return None

        return user


user_repo = UserRepository()
