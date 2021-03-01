import base64

from cryptography.fernet import Fernet


class ActivationTokenEncoder:

    def __init__(self, key: str):
        self._fernet = Fernet(key=key.encode())

    def encode_token(self, email: str) -> str:
        encrypted_data = self._fernet.encrypt(base64.urlsafe_b64encode(email.encode()))
        activation_token = base64.urlsafe_b64encode(encrypted_data).decode()
        return activation_token

    def decode_token(self, activation_token: str) -> str:
        decoded_token = str(base64.urlsafe_b64decode(activation_token.encode()))
        data = self._fernet.decrypt(bytes(decoded_token))
        return str(data)
