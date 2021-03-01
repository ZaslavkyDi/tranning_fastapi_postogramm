from pathlib import Path
from typing import Any

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_user_post_owner
from app.models.user import User

router = APIRouter(
    tags=['posts']
)


@router.get('/{post_id}')
async def get_post(post_id: int = Path(...)) -> Any:
    pass


@router.get('')
async def get_posts(db: Session = Depends(get_db)) -> Any:
    pass


@router.put('/{post_id}')
async def update_post(
        db: Session = Depends(get_db),
        post_id: int = Path(...),
        post_owner: User = Depends(get_user_post_owner)
) -> Any:
    pass
