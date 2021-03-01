from app.models.post import Post
from app.repositories.base import BaseRepository
from app.schemas.post import PostCreate, PostUpdate


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):

    def __init__(self):
        super().__init__(model_type=Post)


post_repo = PostRepository()
