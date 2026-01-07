# app/services/historial_vacunacion_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.historial_vacunacion import HistorialVacunacion
from ..schemas.historial_vacunacion import HistorialVacunacionCreate, HistorialVacunacionUpdate

def crear_historial(db: Session, data: HistorialVacunacionCreate) -> HistorialVacunacion:
    h = HistorialVacunacion(**data.dict())
    db.add(h)
    db.commit()
    db.refresh(h)
    return h

def listar_historiales(db: Session) -> List[HistorialVacunacion]:
    return db.query(HistorialVacunacion).filter(HistorialVacunacion.activo == True).all()

def obtener_historial(db: Session, id_historial: int) -> Optional[HistorialVacunacion]:
    return db.query(HistorialVacunacion).filter(HistorialVacunacion.id_historial == id_historial).first()

def actualizar_historial(db: Session, id_historial: int, data: HistorialVacunacionUpdate) -> Optional[HistorialVacunacion]:
    h = obtener_historial(db, id_historial)
    if not h:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(h, key, value)
    db.commit()
    db.refresh(h)
    return h

def desactivar_historial(db: Session, id_historial: int) -> bool:
    h = obtener_historial(db, id_historial)
    if not h:
        return False
    h.activo = False
    db.commit()
    return True
