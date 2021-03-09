from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
