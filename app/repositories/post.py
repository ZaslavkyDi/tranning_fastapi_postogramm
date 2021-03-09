from typing import Optional

from sqlalchemy.orm import Session

from app.entities.post import Post
from app.entities.user import User
from app.models.post import PostCreate, PostUpdate
from app.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):

    def __init__(self):
        super().__init__(model_type=Post)

    def get_post_by_id_and_author(self, db: Session, /, id: int, author: User) -> Optional[Post]:
        return db.query(self.model_type) \
            .filter(self.model_type.id == id) \
            .filter(self.model_type.author == author) \
            .firs()


post_repo = PostRepository()
