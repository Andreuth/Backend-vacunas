# app/services/persona_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException

from ..models.persona import Persona
from ..schemas.persona import PersonaCreate, PersonaUpdate
from ..security.hashing import get_password_hash


ROLES = {"admin", "medico", "padre", "hijo"}


def _validar_rol_creacion(current_user: Persona, rol_nuevo: str):
    # Médico solo puede crear padre/hijo
    if current_user.rol == "medico" and rol_nuevo not in {"padre", "hijo"}:
        raise HTTPException(status_code=403, detail="Médico solo puede crear usuarios padre o hijo.")


def _validar_rol_actualizacion(current_user: Persona, rol_nuevo: str):
    # Médico no puede elevar roles a admin/medico
    if current_user.rol == "medico" and rol_nuevo in {"admin", "medico"}:
        raise HTTPException(status_code=403, detail="Médico no puede asignar rol admin o medico.")


def _validar_documento_unico(db: Session, numero_documento: str, excluir_id: Optional[int] = None):
    q = db.query(Persona).filter(Persona.numero_documento == numero_documento)
    if excluir_id:
        q = q.filter(Persona.id_persona != excluir_id)
    if q.first():
        raise HTTPException(status_code=409, detail="Ya existe una persona con ese número de documento.")


# ---------------------------
# CREAR
# ---------------------------
def crear_persona(db: Session, data: PersonaCreate, current_user: Persona) -> Persona:
    if data.rol not in ROLES:
        raise HTTPException(status_code=400, detail="Rol inválido.")

    _validar_rol_creacion(current_user, data.rol)

    # documento único
    _validar_documento_unico(db, data.numero_documento)

    # hijo -> sin contraseña
    password_hash = None
    if data.rol != "hijo":
        if not getattr(data, "password", None):
            raise HTTPException(status_code=400, detail="Password es obligatorio para roles que no sean hijo.")
        password_hash = get_password_hash(data.password)

    persona = Persona(
        nombres=data.nombres,
        apellidos=data.apellidos,
        numero_documento=data.numero_documento,
        rol=data.rol,
        password_hash=password_hash,
        # ✅ sin auditoría porque tu tabla/modelo Persona no tiene esos campos
    )

    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona


# ---------------------------
# LISTAR
# ---------------------------
def listar_personas(db: Session, current_user: Persona) -> List[Persona]:
    q = db.query(Persona).filter(Persona.activo == True)

    # Médico solo ve padre e hijo
    if current_user.rol == "medico":
        q = q.filter(Persona.rol.in_(["padre", "hijo"]))

    return q.all()


# ---------------------------
# OBTENER
# ---------------------------
def obtener_persona(db: Session, id_persona: int, current_user: Persona) -> Optional[Persona]:
    persona = (
        db.query(Persona)
        .filter(Persona.id_persona == id_persona, Persona.activo == True)
        .first()
    )
    if not persona:
        return None

    # Médico solo puede acceder padre/hijo
    if current_user.rol == "medico" and persona.rol not in ["padre", "hijo"]:
        return None

    return persona


# ---------------------------
# ACTUALIZAR
# ---------------------------
def actualizar_persona(db: Session, id_persona: int, data: PersonaUpdate, current_user: Persona) -> Optional[Persona]:
    persona = obtener_persona(db, id_persona, current_user)
    if not persona:
        return None

    payload = data.dict(exclude_unset=True)

    # documento único si se cambia
    if "numero_documento" in payload and payload["numero_documento"] != persona.numero_documento:
        _validar_documento_unico(db, payload["numero_documento"], excluir_id=id_persona)

    # si cambian rol -> aplicar reglas
    if "rol" in payload:
        if payload["rol"] not in ROLES:
            raise HTTPException(status_code=400, detail="Rol inválido.")
        _validar_rol_actualizacion(current_user, payload["rol"])

        # si cambia a hijo -> borrar password
        if payload["rol"] == "hijo":
            payload["password_hash"] = None

    # si viene password
    if "password" in payload:
        if persona.rol == "hijo":
            raise HTTPException(status_code=400, detail="No se asigna password a rol hijo.")
        payload["password_hash"] = get_password_hash(payload["password"])
        del payload["password"]

    for key, value in payload.items():
        setattr(persona, key, value)

    db.commit()
    db.refresh(persona)
    return persona


# ---------------------------
# DESACTIVAR
# ---------------------------
def desactivar_persona(db: Session, id_persona: int, current_user: Persona) -> bool:
    persona = obtener_persona(db, id_persona, current_user)
    if not persona:
        return False

    persona.activo = False
    db.commit()
    return True
