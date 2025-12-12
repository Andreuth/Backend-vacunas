from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    numero_documento: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id_persona: Optional[int] = None
    numero_documento: Optional[str] = None
