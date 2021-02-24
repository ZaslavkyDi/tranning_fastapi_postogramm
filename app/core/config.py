from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str = 'secret'

    MIN_USER_AGE: int = 18
    DB_URL: str = 'sqlite:///../database.db'


settings = Settings()
