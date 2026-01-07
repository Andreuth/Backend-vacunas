from sqlalchemy.orm import Session
from ..models.persona import Persona
from ..security.hashing import verify_password

def authenticate_user(db: Session, numero_documento: str, password: str) -> Persona | None:
    user = db.query(Persona).filter(
        Persona.numero_documento == numero_documento,
        Persona.activo == True
    ).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
