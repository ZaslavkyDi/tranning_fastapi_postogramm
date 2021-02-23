from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.settings import Settings

engine = create_engine(Settings.DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
