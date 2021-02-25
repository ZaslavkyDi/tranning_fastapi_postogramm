from typing import List, Optional, Any

import fastapi
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Path, Body
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

import app.schemas.user as schemas
from app.dependencies import get_db
from app.repositories.user import user_repo

router = APIRouter(
    tags=['users']
)


@router.get('', response_model=List[schemas.User])
async def get_users(
        db: Session = Depends(get_db),
        skip: Optional[int] = 0,
        limit: Optional[int] = 0
) -> Any:
    if limit == 0:
        users = user_repo.get_all(db)
    else:
        users = user_repo.get_multi(db, skip=skip, limit=limit)

    return users


@router.get('/{id}', response_model=schemas.User)
async def get_user_by_id(db: Session = Depends(get_db), id: int = Path(...)) -> Any:
    return user_repo.get_by_email(db, id=id)


@router.post('', response_model=schemas.User)
async def create_user(
        db: Session = Depends(get_db),
        user_schema: schemas.UserCreate = Body(...)
) -> Any:
    user = user_repo.get_by_email(db, email=user_schema.email)
    if user:
        raise HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail='User already exists'
        )

    return user_repo.create(db, dto_schema=user_schema)


@router.put('/{id}', response_model=schemas.User)
async def update_user(
        db: Session = Depends(get_db),
        id: int = Path(...),
        user_schema: schemas.UserUpdate = Body(...)
) -> Any:
    saved_user = user_repo.get(db, id=id)
    if not saved_user:
        raise HTTPException(status_code=404, detail="User not found")

    return user_repo.update(db, entity=saved_user, dto_schema=user_schema)


@router.delete('/{id}', response_model=schemas.User)
async def delete_user(db: Session = Depends(get_db), id: int = Path(...)) -> Any:
    return user_repo.delete(db, id=id)
