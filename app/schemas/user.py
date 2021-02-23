import datetime
from typing import Optional

from fastapi.exceptions import HTTPException
from pydantic.class_validators import validator
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from starlette.status import HTTP_409_CONFLICT

from ..core.config import settings


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = False
    is_superuser: bool = False
    birth_date: Optional[datetime.date] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str
    birth_date: datetime.date

    @validator('birth_date', pre=True)
    def check_user_age(cls, value: str) -> datetime.date:
        birth_date = datetime.datetime.strptime(value, '%Y-%m-%d')
        today = datetime.date.today()

        user_age = today.year - birth_date.year

        if settings.MIN_USER_AGE > user_age:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=f"User's age less then {settings.MIN_USER_AGE}!"
            )

        return birth_date


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    """
    Additional properties to return via API
    """
    pass
