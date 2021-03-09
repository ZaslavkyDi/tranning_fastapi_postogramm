from typing import Any, List

from fastapi import APIRouter, Path
from fastapi.params import Depends, Body

from app.api.services.posts import PostService
from app.dependencies.user import get_user_post_owner, get_current_active_user
from app.entities.user import User
from app.models.post import PostCreate, PostOutDB, PostUpdate

router = APIRouter(
    tags=['posts'],
    dependencies=[Depends(get_current_active_user)]
)


@router.post('', response_model=PostOutDB, operation_id="authorize")
async def create_post(
        create_schema: PostCreate = Body(...),
        current_user: User = Depends(get_current_active_user),
        post_service: PostService = Depends(),
) -> Any:
    saved_post = post_service.create_post(create_schema=create_schema, current_user=current_user)
    out_dto_post = PostOutDB.from_orm(saved_post)
    return out_dto_post


@router.get('/{post_id}', response_model=PostOutDB, operation_id="authorize")
async def get_post(
        post_id: int = Path(...),
        post_service: PostService = Depends()
) -> Any:
    post = post_service.get_post_by_id(post_id)
    return post


@router.get('', response_model=List[PostOutDB], operation_id="authorize")
async def get_posts(
        current_user: User = Depends(get_current_active_user),
        post_service: PostService = Depends(),
) -> Any:
    user_posts = post_service.get_user_posts(user=current_user)
    return user_posts


@router.put('/{post_id}', response_model=PostOutDB, operation_id="authorize")
async def update_post(
        post_id: int = Path(...),
        update_schema: PostUpdate = Body(...),
        post_owner: User = Depends(get_user_post_owner),
        post_service: PostService = Depends(),
) -> Any:
    updated_post = post_service.update_post(
        post_id=post_id,
        update_schema=update_schema
    )
    return updated_post


@router.delete('/{post_id}', response_model=PostOutDB, operation_id="authorize")
async def delete_post(
        post_id: int = Path(...),
        post_owner: User = Depends(get_user_post_owner),
        post_service: PostService = Depends(),
) -> Any:
    deleted_post = post_service.delete_post(post_id=post_id)
    return deleted_post
