from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Date

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    birth_day = Column(Date, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
