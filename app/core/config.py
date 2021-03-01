from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str = '0FB5ZdvjC3M3E6ohIvQgRSDAnbkbTtKBE6MVVZj92JM='

    MIN_USER_AGE: int = 18
    DB_URL: str = 'sqlite:///../database.db'


settings = Settings()
