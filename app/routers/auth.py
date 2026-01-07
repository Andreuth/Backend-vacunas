from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from ..schemas.auth import Token
from ..services.auth_service import authenticate_user
from ..security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # usamos username como numero_documento
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Número de documento o contraseña incorrectos"
        )

    access_token = create_access_token(user.id_persona)
    return {
    "access_token": access_token,
    "token_type": "bearer",
    "rol": user.rol
}

