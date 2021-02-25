from typing import Optional

from pydantic.main import BaseModel


class Tokens(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
