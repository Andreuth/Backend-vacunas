<<<<<<< HEAD
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.tipos_vacunas import TipoVacuna
from ..schemas.tipos_vacunas import TipoVacunaCreate, TipoVacunaUpdate
from ..models.persona import Persona


# ---------------------------
# CREAR
# ---------------------------
def crear_vacuna(db: Session, data: TipoVacunaCreate, current_user: Persona) -> TipoVacuna:
    vacuna = TipoVacuna(
        **data.dict(),
        id_usuario_creo=current_user.id_persona,        # ✅ auditoría
        id_usuario_actualizo=current_user.id_persona,   # ✅ auditoría
    )
    db.add(vacuna)
    db.commit()
    db.refresh(vacuna)
    return vacuna


# ---------------------------
# LISTAR
# ---------------------------
def listar_vacunas(db: Session) -> List[TipoVacuna]:
    return db.query(TipoVacuna).filter(TipoVacuna.activo == True).all()


# ---------------------------
# OBTENER
# ---------------------------
def obtener_vacuna(db: Session, id_vacuna: int) -> Optional[TipoVacuna]:
    return db.query(TipoVacuna).filter(TipoVacuna.id_vacuna == id_vacuna).first()


# ---------------------------
# ACTUALIZAR
# ---------------------------
def actualizar_vacuna(
    db: Session,
    id_vacuna: int,
    data: TipoVacunaUpdate,
    current_user: Persona
) -> Optional[TipoVacuna]:

    vacuna = obtener_vacuna(db, id_vacuna)
    if not vacuna or not vacuna.activo:
        return None

    # actualizar solo campos enviados
    for key, value in data.dict(exclude_unset=True).items():
        setattr(vacuna, key, value)

    vacuna.id_usuario_actualizo = current_user.id_persona   # ✅ auditoría

    db.commit()
    db.refresh(vacuna)
    return vacuna


# ---------------------------
# DESACTIVAR
# ---------------------------
def desactivar_vacuna(db: Session, id_vacuna: int) -> bool:
    vacuna = obtener_vacuna(db, id_vacuna)
    if not vacuna:
        return False

    vacuna.activo = False
    db.commit()
    return True

=======
# app/services/tipos_vacunas_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.tipos_vacunas import TipoVacuna
from ..schemas.tipos_vacunas import TipoVacunaCreate, TipoVacunaUpdate

def crear_vacuna(db: Session, data: TipoVacunaCreate) -> TipoVacuna:
    vacuna = TipoVacuna(**data.dict())
    db.add(vacuna)
    db.commit()
    db.refresh(vacuna)
    return vacuna

def listar_vacunas(db: Session) -> List[TipoVacuna]:
    return db.query(TipoVacuna).filter(TipoVacuna.activo == True).all()

def obtener_vacuna(db: Session, id_vacuna: int) -> Optional[TipoVacuna]:
    return db.query(TipoVacuna).filter(TipoVacuna.id_vacuna == id_vacuna).first()

def actualizar_vacuna(db: Session, id_vacuna: int, data: TipoVacunaUpdate) -> Optional[TipoVacuna]:
    vacuna = obtener_vacuna(db, id_vacuna)
    if not vacuna:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(vacuna, key, value)
    db.commit()
    db.refresh(vacuna)
    return vacuna

def desactivar_vacuna(db: Session, id_vacuna: int) -> bool:
    vacuna = obtener_vacuna(db, id_vacuna)
    if not vacuna:
        return False
    vacuna.activo = False
    db.commit()
    return True
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
