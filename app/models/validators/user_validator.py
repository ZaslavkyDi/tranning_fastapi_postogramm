import datetime
from typing import Union

from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT

from app.core.config import settings


def check_user_age(value: Union[datetime.datetime, str]) -> datetime.date:
    if isinstance(value, str):
        birth_date = datetime.datetime.strptime(value, '%Y-%m-%d')
    else:
        birth_date = value

    today = datetime.date.today()
    user_age = today.year - birth_date.year

    if settings.min_user_age > user_age:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"User's age less then {settings.min_user_age}!"
        )

    return value
