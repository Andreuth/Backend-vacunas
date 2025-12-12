from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from ..core.config import settings
from ..database import get_db
from ..models.persona import Persona

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Creamos SIEMPRE un token con:
#   sub = id de persona (como string)
#   exp = fecha de expiración
def create_access_token(
    user_id: int,
    expires_minutes: Optional[int] = None
) -> str:
    if expires_minutes is None:
        expires_minutes = settings.access_token_expire_minutes

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Persona:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception

        # sub venía como str, lo convertimos a int
        user_id = int(sub)
    except (JWTError, ValueError):
        # JWT incorrecto, expirado o sub no convertible a int
        raise credentials_exception

    user = db.query(Persona).filter(
        Persona.id_persona == user_id,
        Persona.activo == True
    ).first()

    if user is None:
        raise credentials_exception

    return user
