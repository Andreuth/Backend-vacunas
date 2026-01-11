from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dateutil.relativedelta import relativedelta

from app.core.deps import get_db
from app.core.deps_auth import require_roles, get_current_user
from app.core.security import hash_password

from app.models.user import User
from app.models.child import Child
from app.models.parent_child import ParentChild

from app.models.vaccine_schedule import VaccineSchedule
from app.models.vaccine import Vaccine
from app.models.vaccine_application import VaccineApplication

from app.schemas.register import RegisterChildRequest, RegisterChildResponse
from app.schemas.child import ChildOut
from app.schemas.next_vaccines import NextVaccinesResponse, NextVaccineItem

from app.services.access import is_child_of_parent

router = APIRouter()

# ==========================
# Registro rápido (ADMIN/PEDIATRA)
# ==========================
@router.post(
    "/register",
    response_model=RegisterChildResponse,
    dependencies=[Depends(require_roles(["ADMIN", "PEDIATRA"]))],
)
def register_child(
    payload: RegisterChildRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sexo = payload.nino.sexo.upper()
    if sexo not in ["M", "F", "OTRO"]:
        raise HTTPException(status_code=400, detail="Sexo inválido. Use M, F u OTRO.")

    # 1) Representante
    rep = (
        db.query(User)
        .filter(User.numero_documento == payload.representante.numero_documento)
        .first()
    )
    if rep:
        if rep.rol != "REPRESENTANTE":
            raise HTTPException(
                status_code=400,
                detail="El documento ya existe pero no es REPRESENTANTE.",
            )
    else:
        rep = User(
            nombres=payload.representante.nombres,
            apellidos=payload.representante.apellidos,
            numero_documento=payload.representante.numero_documento,
            password_hash=hash_password(payload.representante.password),
            rol="REPRESENTANTE",
            created_by=current_user.id,
        )
        db.add(rep)
        db.flush()

    # 2) Niño
    exists_child = (
        db.query(Child)
        .filter(Child.numero_documento == payload.nino.numero_documento)
        .first()
    )
    if exists_child:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un niño con ese número de documento.",
        )

    child = Child(
        nombres=payload.nino.nombres,
        apellidos=payload.nino.apellidos,
        numero_documento=payload.nino.numero_documento,
        fecha_nacimiento=payload.nino.fecha_nacimiento,
        sexo=sexo,
    )
    db.add(child)
    db.flush()

    # 3) Relación
    rel_exists = (
        db.query(ParentChild)
        .filter(
            ParentChild.parent_id == rep.id,
            ParentChild.child_id == child.id,
        )
        .first()
    )
    if rel_exists:
        raise HTTPException(
            status_code=400,
            detail="La relación representante-niño ya existe.",
        )

    rel = ParentChild(
        parent_id=rep.id,
        child_id=child.id,
        parentesco=payload.parentesco,
        es_principal=payload.es_principal,
    )
    db.add(rel)

    db.commit()
    db.refresh(rep)
    db.refresh(child)
    db.refresh(rel)

    return RegisterChildResponse(
        representante_id=rep.id,
        nino_id=child.id,
        relacion_id=rel.id,
    )


# ==========================
# Representante: ver SOLO mis hijos
# ==========================
@router.get(
    "/my",
    response_model=list[ChildOut],
    dependencies=[Depends(require_roles(["REPRESENTANTE"]))],
)
def my_children(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = (
        db.query(Child)
        .join(ParentChild, ParentChild.child_id == Child.id)
        .filter(ParentChild.parent_id == current_user.id, Child.activo == True)
        .all()
    )
    return rows


# ==========================
# Próximas vacunas
# ==========================
@router.get(
    "/{child_id}/next-vaccines",
    response_model=NextVaccinesResponse,
    dependencies=[Depends(require_roles(["ADMIN", "PEDIATRA", "REPRESENTANTE"]))],
)
def next_vaccines(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Si es representante, validar relación
    if current_user.rol == "REPRESENTANTE":
        if not is_child_of_parent(db, current_user.id, child_id):
            raise HTTPException(status_code=403, detail="No autorizado para ver este niño")

    child = (
        db.query(Child)
        .filter(Child.id == child_id, Child.activo == True)
        .first()
    )
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")

    # Dosis ya aplicadas
    applied_schedule_ids = {
        row[0]
        for row in db.query(VaccineApplication.schedule_id)
        .filter(
            VaccineApplication.child_id == child_id,
            VaccineApplication.activo == True,
        )
        .all()
    }

    # Todo el esquema
    rows = (
        db.query(VaccineSchedule, Vaccine)
        .join(Vaccine, Vaccine.id == VaccineSchedule.vaccine_id)
        .filter(
            VaccineSchedule.activo == True,
            Vaccine.activo == True,
        )
        .order_by(Vaccine.nombre.asc(), VaccineSchedule.dosis_numero.asc())
        .all()
    )

    today = date.today()
    items: list[NextVaccineItem] = []

    for sch, vac in rows:
        if sch.id in applied_schedule_ids:
            continue

        fecha_recomendada = child.fecha_nacimiento + relativedelta(
            months=+sch.edad_objetivo_meses
        )

        dias_diff = (fecha_recomendada - today).days
        estado = "PENDIENTE" if dias_diff >= 0 else "ATRASADA"

        items.append(
            NextVaccineItem(
                vaccine_id=vac.id,
                vaccine_nombre=vac.nombre,
                schedule_id=sch.id,
                dosis_numero=sch.dosis_numero,
                edad_objetivo_meses=sch.edad_objetivo_meses,
                fecha_recomendada=fecha_recomendada,
                estado=estado,
                dias_diferencia=dias_diff,
            )
        )

    return NextVaccinesResponse(child_id=child_id, items=items)


# ==========================
# Listar niños (ADMIN / PEDIATRA)
# ==========================
@router.get(
    "/",
    response_model=list[ChildOut],
    dependencies=[Depends(require_roles(["ADMIN", "PEDIATRA"]))],
)
def list_children(db: Session = Depends(get_db)):
    return (
        db.query(Child)
        .filter(Child.activo == True)
        .order_by(Child.id.desc())
        .all()
    )
