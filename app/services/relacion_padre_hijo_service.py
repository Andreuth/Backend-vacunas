# app/services/relacion_padre_hijo_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.relacion_padre_hijo import RelacionPadreHijo
from ..schemas.relacion_padre_hijo import RelacionCreate, RelacionUpdate

def crear_relacion(db: Session, data: RelacionCreate) -> RelacionPadreHijo:
    r = RelacionPadreHijo(**data.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

def listar_relaciones(db: Session) -> List[RelacionPadreHijo]:
    return db.query(RelacionPadreHijo).filter(RelacionPadreHijo.activo == True).all()

def obtener_relacion(db: Session, id_relacion: int) -> Optional[RelacionPadreHijo]:
    return db.query(RelacionPadreHijo).filter(RelacionPadreHijo.id_relacion == id_relacion).first()

def actualizar_relacion(db: Session, id_relacion: int, data: RelacionUpdate) -> Optional[RelacionPadreHijo]:
    r = obtener_relacion(db, id_relacion)
    if not r:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(r, key, value)
    db.commit()
    db.refresh(r)
    return r

def desactivar_relacion(db: Session, id_relacion: int) -> bool:
    r = obtener_relacion(db, id_relacion)
    if not r:
        return False
    r.activo = False
    db.commit()
    return True
