import os

import dotenv
from pydantic.env_settings import BaseSettings

env_file_path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(env_file_path)


class Settings(BaseSettings):
    authjwt_secret_key: str = os.getenv('JWT_SECRET')

    MIN_USER_AGE: int = os.getenv('MIN_USER_AGE')
    DB_URL: str = os.getenv('DB_URL')


settings = Settings()
