from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.core.deps_auth import get_current_user   # 👈 IMPORTANTE
from app.schemas.auth import LoginRequest, Token
from app.schemas.me import MeOut                  # 👈 IMPORTANTE
from app.models.user import User

router = APIRouter()

# =========================
# Login JSON (para el front)
# =========================
@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.numero_documento == data.numero_documento,
        User.activo == True
    ).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(
        subject=user.numero_documento,
        secret_key=settings.SECRET_KEY,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(access_token=token)


# ==========================================
# Login para Swagger Authorize (OAuth2 flow)
# ==========================================
@router.post("/token", response_model=Token)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.numero_documento == form_data.username,
        User.activo == True
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(
        subject=user.numero_documento,
        secret_key=settings.SECRET_KEY,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(access_token=token)


# =========================
# Usuario autenticado
# =========================
@router.get("/me", response_model=MeOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
