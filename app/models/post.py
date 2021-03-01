from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Text, DateTime

from app.db.base_class import Base


class Post(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(Text)
    published_date = Column(DateTime, server_default=func.now(), nullable=False)
    updated_date = Column(DateTime, onupdate=func.now(), nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates='posts')
