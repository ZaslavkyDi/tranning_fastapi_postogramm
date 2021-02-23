from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    MIN_USER_AGE: int = 18
    DB_URL: str = 'sqlite:///database.db'
