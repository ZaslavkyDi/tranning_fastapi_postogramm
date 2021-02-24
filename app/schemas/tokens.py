from typing import Optional

from pydantic.main import BaseModel


class TokenSchema(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
