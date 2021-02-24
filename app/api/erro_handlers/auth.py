from typing import Any

from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Body
from fastapi_jwt_auth.auth_jwt import AuthJWT

from app.db.session import SessionLocal
from app.main import app
from app.repositories.user import user_repo
from app.schemas.tokens import TokenSchema
from app.schemas.user import User


@app.post('/login', response_model=TokenSchema)
async def login(
        db: SessionLocal = Depends(),
        authorize: AuthJWT = Depends(),
        user: User = Body(...),
) -> Any:
    saved_user = user_repo.get_by_email(db, email=user.email)
    if not saved_user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = authorize.create_access_token(subject=user.email)
    return TokenSchema(
        access_token=access_token
    )
