from sqlalchemy.orm.session import Session


def init_db(db: Session) -> None:
    """
    Tables should be created by Alembic migrations
    """
    pass
