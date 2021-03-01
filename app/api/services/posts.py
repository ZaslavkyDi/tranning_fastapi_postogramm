from typing import List

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.post import Post
from app.models.user import User
from app.repositories.post import post_repo
from app.repositories.user import user_repo
from app.schemas.post import PostCreate, PostUpdate


class PostService:

    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    def create_post(self, create_schema: PostCreate, current_user: User) -> Post:
        saved_post = post_repo.create(
            self._db,
            dto_schema=create_schema,
        )
        saved_post.author = current_user
        saved_post.author_id = current_user.id

        current_user.posts.append(saved_post)

        post_repo.save_or_update(self._db, entity=saved_post)
        user_repo.save_or_update(self._db, entity=current_user)

        return saved_post

    def get_post_by_id(self, post_id: int) -> Post:
        return post_repo.get(self._db, id=post_id)

    @staticmethod
    def get_user_posts(user: User) -> List[Post]:
        return user.posts

    def update_post(self, post_id: int, update_schema: PostUpdate) -> Post:
        saved_post = post_repo.get(self._db, id=post_id)
        updated_post = post_repo.update(self._db, entity=saved_post, dto_schema=update_schema)
        return updated_post

    def delete_post(self, post_id: int) -> Post:
        deleted_post = post_repo.delete(self._db, id=post_id)
        return deleted_post
