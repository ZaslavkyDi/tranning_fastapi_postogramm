import datetime
from typing import Optional

from pydantic.class_validators import validator
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from ..core.config import Settings


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
    def check_user_age(cls, value: datetime.date) -> datetime.date:
        today = datetime.date.today()
        user_age = today.year - value.year

        if Settings.MIN_USER_AGE > user_age:
            raise AttributeError(f"User' age less then {Settings.MIN_USER_AGE}!")

        return value


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
