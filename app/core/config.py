import os

import dotenv
from pydantic.env_settings import BaseSettings

env_file_path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(env_file_path)


class Settings(BaseSettings):
    # openssl rand -hex 32
    authjwt_secret_key: str = os.getenv('JWT_SECRET')
    authjwt_algorithm: str = 'HS256'
    activate_token_expire_hours: int = os.getenv('ACTIVATE_TOKEN_EXPIRE_HOURS')

    min_user_age: int = os.getenv('MIN_USER_AGE')
    db_url: str = os.getenv('DB_URL')

    smtp_server: str = os.getenv('SMTP_SERVER')
    smtp_server_port: int = os.getenv('SMTP_SERVER_PORT')
    email_sender: str = os.getenv('EMAIL_SENDER')
    email_password: str = os.getenv('EMAIL_PASSWORD')


class CelerySettings(BaseSettings):
    backend_url = os.getenv('CELERY_BACKEND_URL')
    broker_url = os.getenv('CELERY_BROKER_URL')


settings = Settings()
celery_settings = CelerySettings()
