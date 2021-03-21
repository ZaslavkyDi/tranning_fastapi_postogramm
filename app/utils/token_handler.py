from datetime import datetime, timedelta
from typing import Dict

from jose import jwt

from app.core.config import settings


class TokenHandler:

    @staticmethod
    def encode_token(data: Dict) -> str:
        if 'exp' not in data:
            data['exp'] = datetime.utcnow() + timedelta(hours=settings.activate_token_expire_hours)

        return jwt.encode(
            claims=data,
            key=settings.authjwt_secret_key,
            algorithm=settings.authjwt_algorithm
        )

    @staticmethod
    def decode_token(activation_token: str) -> Dict:
        return jwt.decode(
            token=activation_token,
            key=settings.authjwt_secret_key,
            algorithms=[settings.authjwt_algorithm]
        )
