<<<<<<< HEAD
# app/services/cargos_medicos_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.cargos_medicos import CargoMedico
from ..schemas.cargos_medicos import CargoMedicoCreate, CargoMedicoUpdate

def crear_cargo(db: Session, data: CargoMedicoCreate) -> CargoMedico:
    cargo = CargoMedico(**data.dict())
    db.add(cargo)
    db.commit()
    db.refresh(cargo)
    return cargo

def listar_cargos(db: Session) -> List[CargoMedico]:
    return db.query(CargoMedico).filter(CargoMedico.activo == True).all()

def obtener_cargo(db: Session, id_cargo: int) -> Optional[CargoMedico]:
    return db.query(CargoMedico).filter(CargoMedico.id_cargo == id_cargo).first()

def actualizar_cargo(db: Session, id_cargo: int, data: CargoMedicoUpdate) -> Optional[CargoMedico]:
    cargo = obtener_cargo(db, id_cargo)
    if not cargo:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(cargo, key, value)
    db.commit()
    db.refresh(cargo)
    return cargo

def desactivar_cargo(db: Session, id_cargo: int) -> bool:
    cargo = obtener_cargo(db, id_cargo)
    if not cargo:
        return False
    cargo.activo = False
    db.commit()
    return True
=======
# app/services/cargos_medicos_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.cargos_medicos import CargoMedico
from ..schemas.cargos_medicos import CargoMedicoCreate, CargoMedicoUpdate

def crear_cargo(db: Session, data: CargoMedicoCreate) -> CargoMedico:
    cargo = CargoMedico(**data.dict())
    db.add(cargo)
    db.commit()
    db.refresh(cargo)
    return cargo

def listar_cargos(db: Session) -> List[CargoMedico]:
    return db.query(CargoMedico).filter(CargoMedico.activo == True).all()

def obtener_cargo(db: Session, id_cargo: int) -> Optional[CargoMedico]:
    return db.query(CargoMedico).filter(CargoMedico.id_cargo == id_cargo).first()

def actualizar_cargo(db: Session, id_cargo: int, data: CargoMedicoUpdate) -> Optional[CargoMedico]:
    cargo = obtener_cargo(db, id_cargo)
    if not cargo:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(cargo, key, value)
    db.commit()
    db.refresh(cargo)
    return cargo

def desactivar_cargo(db: Session, id_cargo: int) -> bool:
    cargo = obtener_cargo(db, id_cargo)
    if not cargo:
        return False
    cargo.activo = False
    db.commit()
    return True
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
