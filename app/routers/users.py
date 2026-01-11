from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import hash_password
from app.core.deps_auth import require_roles, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserCreateRepresentative

router = APIRouter()

# =========================
# ADMIN: CRUD TOTAL USUARIOS
# =========================

@router.get("/", response_model=list[UserOut], dependencies=[Depends(require_roles(["ADMIN"]))])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/", response_model=UserOut, dependencies=[Depends(require_roles(["ADMIN"]))])
def create_user(payload: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Admin puede crear cualquier rol
    if payload.rol not in ["ADMIN", "PEDIATRA", "REPRESENTANTE"]:
        raise HTTPException(status_code=400, detail="Rol inválido")

    exists = db.query(User).filter(User.numero_documento == payload.numero_documento).first()
    if exists:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese documento")

    user = User(
        nombres=payload.nombres,
        apellidos=payload.apellidos,
        numero_documento=payload.numero_documento,
        password_hash=hash_password(payload.password),
        rol=payload.rol,
        created_by=current_user.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ==========================================
# PEDIATRA: Crear SOLO REPRESENTANTES (rápido)
# ==========================================

@router.post("/representatives", response_model=UserOut, dependencies=[Depends(require_roles(["ADMIN","PEDIATRA"]))])
def create_representative(payload: UserCreateRepresentative, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Si es pediatra, SOLO puede crear representantes
    # Si es admin, también puede usar este endpoint, pero crea representante igual
    exists = db.query(User).filter(User.numero_documento == payload.numero_documento).first()
    if exists:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese documento")

    rep = User(
        nombres=payload.nombres,
        apellidos=payload.apellidos,
        numero_documento=payload.numero_documento,
        password_hash=hash_password(payload.password),
        rol="REPRESENTANTE",
        created_by=current_user.id
    )
    db.add(rep)
    db.commit()
    db.refresh(rep)
    return rep
