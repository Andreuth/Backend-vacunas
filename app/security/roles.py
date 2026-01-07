# app/security/roles.py
from typing import List
from fastapi import Depends, HTTPException, status

from .jwt import get_current_user
from ..models.persona import Persona

def require_roles(allowed_roles: List[str]):
    """
    Dependencia para proteger endpoints por rol.
    Si el rol del usuario no está permitido => 403.
    """
    def role_checker(current_user: Persona = Depends(get_current_user)) -> Persona:
        if current_user.rol not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permisos. Roles permitidos: {allowed_roles}"
            )
        return current_user
    return role_checker

