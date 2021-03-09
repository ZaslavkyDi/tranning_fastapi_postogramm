from pydantic import BaseModel, EmailStr


class AuthData(BaseModel):
    email: EmailStr
    password: str
