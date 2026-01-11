from pydantic import BaseModel

class LoginRequest(BaseModel):
    numero_documento: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
