from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.persona import Persona
from ..schemas.persona import PersonaCreate, PersonaUpdate
from ..security.hashing import get_password_hash

def crear_persona(db: Session, data: PersonaCreate) -> Persona:
    hashed = get_password_hash(data.password)
    persona = Persona(
        nombres=data.nombres,
        apellidos=data.apellidos,
        numero_documento=data.numero_documento,
        rol=data.rol,
        password_hash=hashed
    )
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona

def listar_personas(db: Session) -> List[Persona]:
    return db.query(Persona).filter(Persona.activo == True).all()

def obtener_persona(db: Session, id_persona: int) -> Optional[Persona]:
    return db.query(Persona).filter(Persona.id_persona == id_persona).first()

def actualizar_persona(db: Session, id_persona: int, data: PersonaUpdate) -> Optional[Persona]:
    persona = obtener_persona(db, id_persona)
    if not persona:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(persona, key, value)
    db.commit()
    db.refresh(persona)
    return persona

def desactivar_persona(db: Session, id_persona: int) -> bool:
    persona = obtener_persona(db, id_persona)
    if not persona:
        return False
    persona.activo = False
    db.commit()
    return True
