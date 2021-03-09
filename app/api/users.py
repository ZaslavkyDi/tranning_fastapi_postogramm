from typing import List, Optional, Any

from fastapi import Query
from fastapi.params import Depends, Path, Body
from fastapi.routing import APIRouter

import app.models.user as schemas
from app.api.services.user import UserService

router = APIRouter(
    tags=['users']
)


@router.get('', response_model=List[schemas.User], operation_id="authorize")
async def get_users(
        skip: Optional[int] = Query(default=0),
        limit: Optional[int] = Query(default=0),
        user_service: UserService = Depends()
) -> Any:
    users = user_service.get_users(skip=skip, limit=limit)
    return users


@router.get('/{user_id}', response_model=schemas.User, operation_id="authorize")
async def get_user_by_id(
        user_id: int = Path(...),
        user_service: UserService = Depends()
) -> Any:
    return user_service.get_user_by_id(user_id=user_id)


@router.post('', response_model=schemas.User, operation_id="authorize")
async def create_user(
        user_schema: schemas.UserCreate = Body(...),
        user_service: UserService = Depends()
) -> Any:
    new_user = user_service.create_user(user_data=user_schema)
    return new_user


@router.put('/{user_id}', response_model=schemas.User, operation_id="authorize")
async def update_user(
        user_id: int = Path(...),
        user_schema: schemas.UserUpdate = Body(...),
        user_service: UserService = Depends()
) -> Any:
    updated_user = user_service.update_user(user_id=user_id, user_data=user_schema)
    return updated_user


@router.delete('/{user_id}', response_model=schemas.User, operation_id="authorize")
async def delete_user(
        user_id: int = Path(...),
        user_service: UserService = Depends()
) -> Any:
    deleted_user = user_service.delete_user(user_id)
    return deleted_user
