import os

import dotenv
from pydantic.env_settings import BaseSettings

env_file_path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(env_file_path)


class Settings(BaseSettings):
    authjwt_secret_key: str = os.getenv('JWT_SECRET')

    min_user_age: int = os.getenv('MIN_USER_AGE')
    db_url: str = os.getenv('DB_URL')

    email_from = os.getenv('EMAIL_FROM')
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')


class CelerySettings(BaseSettings):
    backend_url = os.getenv('CELERY_BACKEND_URL')
    broker_url = os.getenv('CELERY_BROKER_URL')


settings = Settings()
celery_settings = CelerySettings()
