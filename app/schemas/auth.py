<<<<<<< HEAD
from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    numero_documento: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str   # 👈 AÑADIDO (CLAVE)

class TokenData(BaseModel):
    id_persona: Optional[int] = None
    numero_documento: Optional[str] = None
=======
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
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
