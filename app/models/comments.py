import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.post import Post


class CommentBase(BaseModel):
    content: Optional[str]
    author_id: Optional[int]
    post_id: Optional[int]
    published_date: Optional[datetime.datetime]


class CommentCreate(BaseModel):
    content: str
    author_id: int
    post_id: int


class CommentUpdate(CommentCreate):
    content: Optional[str]
    author_id: Optional[int]
    post_id: Optional[int]


class CommentInDBBase(CommentBase):
    id: int


class CommentOutDB(CommentInDBBase):
    pass


class Comment(CommentInDBBase):
    post: Post
