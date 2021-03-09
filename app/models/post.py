import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author_id: Optional[int] = None
    published_date: Optional[datetime.datetime] = None
    updated_date: Optional[datetime.datetime] = None


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(PostCreate):
    title: Optional[str] = None
    content: Optional[str] = None


class PostInDBBase(PostBase):
    id: int

    class Config:
        orm_mode = True


class PostOutDB(PostInDBBase):
    title: Optional[str] = None
    content: Optional[str] = None
    author_id: Optional[int] = None
    published_date: Optional[datetime.datetime] = None
    updated_date: Optional[datetime.datetime] = None


class Post(PostInDBBase):
    """
    Additional properties to return via API
    """
    pass
