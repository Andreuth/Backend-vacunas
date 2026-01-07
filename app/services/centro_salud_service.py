<<<<<<< HEAD
# app/services/centro_salud_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.centro_salud import CentroSalud
from ..schemas.centro_salud import CentroSaludCreate, CentroSaludUpdate

def crear_centro(db: Session, data: CentroSaludCreate) -> CentroSalud:
    centro = CentroSalud(**data.dict())
    db.add(centro)
    db.commit()
    db.refresh(centro)
    return centro

def listar_centros(db: Session) -> List[CentroSalud]:
    return db.query(CentroSalud).filter(CentroSalud.activo == True).all()

def obtener_centro(db: Session, id_centro: int) -> Optional[CentroSalud]:
    return db.query(CentroSalud).filter(CentroSalud.id_centro == id_centro).first()

def actualizar_centro(db: Session, id_centro: int, data: CentroSaludUpdate) -> Optional[CentroSalud]:
    centro = obtener_centro(db, id_centro)
    if not centro:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(centro, key, value)
    db.commit()
    db.refresh(centro)
    return centro

def desactivar_centro(db: Session, id_centro: int) -> bool:
    centro = obtener_centro(db, id_centro)
    if not centro:
        return False
    centro.activo = False
    db.commit()
    return True
=======
# app/services/centro_salud_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.centro_salud import CentroSalud
from ..schemas.centro_salud import CentroSaludCreate, CentroSaludUpdate

def crear_centro(db: Session, data: CentroSaludCreate) -> CentroSalud:
    centro = CentroSalud(**data.dict())
    db.add(centro)
    db.commit()
    db.refresh(centro)
    return centro

def listar_centros(db: Session) -> List[CentroSalud]:
    return db.query(CentroSalud).filter(CentroSalud.activo == True).all()

def obtener_centro(db: Session, id_centro: int) -> Optional[CentroSalud]:
    return db.query(CentroSalud).filter(CentroSalud.id_centro == id_centro).first()

def actualizar_centro(db: Session, id_centro: int, data: CentroSaludUpdate) -> Optional[CentroSalud]:
    centro = obtener_centro(db, id_centro)
    if not centro:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(centro, key, value)
    db.commit()
    db.refresh(centro)
    return centro

def desactivar_centro(db: Session, id_centro: int) -> bool:
    centro = obtener_centro(db, id_centro)
    if not centro:
        return False
    centro.activo = False
    db.commit()
    return True
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
