<<<<<<< HEAD
# app/services/detalle_historial_vacuna_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.detalle_historial_vacuna import DetalleHistorialVacuna
from ..schemas.detalle_historial_vacuna import DetalleHistorialCreate, DetalleHistorialUpdate

def crear_detalle(db: Session, data: DetalleHistorialCreate) -> DetalleHistorialVacuna:
    d = DetalleHistorialVacuna(**data.dict())
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

def listar_detalles(db: Session) -> List[DetalleHistorialVacuna]:
    return db.query(DetalleHistorialVacuna).filter(DetalleHistorialVacuna.activo == True).all()

def obtener_detalle(db: Session, id_detalle: int) -> Optional[DetalleHistorialVacuna]:
    return db.query(DetalleHistorialVacuna).filter(DetalleHistorialVacuna.id_detalle == id_detalle).first()

def actualizar_detalle(db: Session, id_detalle: int, data: DetalleHistorialUpdate) -> Optional[DetalleHistorialVacuna]:
    d = obtener_detalle(db, id_detalle)
    if not d:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(d, key, value)
    db.commit()
    db.refresh(d)
    return d

def desactivar_detalle(db: Session, id_detalle: int) -> bool:
    d = obtener_detalle(db, id_detalle)
    if not d:
        return False
    d.activo = False
    db.commit()
    return True
=======
# app/services/detalle_historial_vacuna_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.detalle_historial_vacuna import DetalleHistorialVacuna
from ..schemas.detalle_historial_vacuna import DetalleHistorialCreate, DetalleHistorialUpdate

def crear_detalle(db: Session, data: DetalleHistorialCreate) -> DetalleHistorialVacuna:
    d = DetalleHistorialVacuna(**data.dict())
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

def listar_detalles(db: Session) -> List[DetalleHistorialVacuna]:
    return db.query(DetalleHistorialVacuna).filter(DetalleHistorialVacuna.activo == True).all()

def obtener_detalle(db: Session, id_detalle: int) -> Optional[DetalleHistorialVacuna]:
    return db.query(DetalleHistorialVacuna).filter(DetalleHistorialVacuna.id_detalle == id_detalle).first()

def actualizar_detalle(db: Session, id_detalle: int, data: DetalleHistorialUpdate) -> Optional[DetalleHistorialVacuna]:
    d = obtener_detalle(db, id_detalle)
    if not d:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(d, key, value)
    db.commit()
    db.refresh(d)
    return d

def desactivar_detalle(db: Session, id_detalle: int) -> bool:
    d = obtener_detalle(db, id_detalle)
    if not d:
        return False
    d.activo = False
    db.commit()
    return True
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
