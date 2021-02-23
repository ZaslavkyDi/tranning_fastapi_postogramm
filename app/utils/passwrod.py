from passlib.context import CryptContext


class BCryptPasswordUtils:
    ENCRYPT_SCHEMAS = ['bcrypt']

    def __init__(self):
        self.crypt_context = CryptContext(schemes=self.ENCRYPT_SCHEMAS, deprecated='auto')

    def encrypt_password(self, password: str) -> str:
        return self.crypt_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.crypt_context.verify(
            secret=password,
            hash=hashed_password
        )
