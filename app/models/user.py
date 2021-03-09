import datetime
from typing import Optional

from pydantic.class_validators import validator
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from .validators.user_validator import check_user_age


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

    _check_user_age_birth_day = validator('birth_date', pre=True, allow_reuse=True)(check_user_age)


class UserRegistrarse(BaseModel):
    email: EmailStr
    password: str
    birth_date: datetime.date
    first_name: str
    last_name: str

    _check_user_age_birth_day = validator('birth_date', pre=True, allow_reuse=True)(check_user_age)


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
