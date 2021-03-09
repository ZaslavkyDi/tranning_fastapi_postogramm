from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Text, DateTime

from app.db.base_class import Base


class Comment(Base):
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    published_date = Column(DateTime, server_default=func.now(), nullable=False)

    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    post = relationship('Post', back_populates='comments')
