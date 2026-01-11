from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.deps_auth import require_roles

from app.models.vaccine import Vaccine
from app.models.vaccine_schedule import VaccineSchedule

from app.schemas.vaccine import VaccineCreate, VaccineOut, ScheduleCreate, ScheduleOut
from app.schemas.vaccine_schedule_full import ScheduleFullOut

router = APIRouter()

# ======================
# VACUNAS (CATÁLOGO)
# ADMIN: CRUD total
# PEDIATRA/REPRESENTANTE: lectura
# ======================

@router.get("/", response_model=list[VaccineOut], dependencies=[Depends(require_roles(["ADMIN","PEDIATRA","REPRESENTANTE"]))])
def list_vaccines(db: Session = Depends(get_db)):
    return db.query(Vaccine).filter(Vaccine.activo == True).all()

@router.post("/", response_model=VaccineOut, dependencies=[Depends(require_roles(["ADMIN"]))])
def create_vaccine(payload: VaccineCreate, db: Session = Depends(get_db)):
    exists = db.query(Vaccine).filter(Vaccine.nombre == payload.nombre).first()
    if exists:
        raise HTTPException(status_code=400, detail="Ya existe una vacuna con ese nombre")
    v = Vaccine(nombre=payload.nombre, descripcion=payload.descripcion)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v

@router.put("/{vaccine_id}", response_model=VaccineOut, dependencies=[Depends(require_roles(["ADMIN"]))])
def update_vaccine(vaccine_id: int, payload: VaccineCreate, db: Session = Depends(get_db)):
    v = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    v.nombre = payload.nombre
    v.descripcion = payload.descripcion
    db.commit()
    db.refresh(v)
    return v

@router.delete("/{vaccine_id}", dependencies=[Depends(require_roles(["ADMIN"]))])
def delete_vaccine(vaccine_id: int, db: Session = Depends(get_db)):
    v = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    v.activo = False
    db.commit()
    return {"ok": True}

# ======================
# ESQUEMA (DOSIS) POR VACUNA
# ADMIN: CRUD total
# PEDIATRA/REPRESENTANTE: lectura
# ======================

@router.get("/schedule", response_model=list[ScheduleOut], dependencies=[Depends(require_roles(["ADMIN","PEDIATRA","REPRESENTANTE"]))])
def list_schedule(db: Session = Depends(get_db)):
    return db.query(VaccineSchedule).filter(VaccineSchedule.activo == True).all()

# ✅ Esquema completo con nombre de vacuna (para admin y pediatra)
@router.get("/schedule/full", response_model=list[ScheduleFullOut], dependencies=[Depends(require_roles(["ADMIN","PEDIATRA"]))])
def list_schedule_full(db: Session = Depends(get_db)):
    rows = (
        db.query(VaccineSchedule, Vaccine)
        .join(Vaccine, Vaccine.id == VaccineSchedule.vaccine_id)
        .filter(VaccineSchedule.activo == True, Vaccine.activo == True)
        .order_by(Vaccine.nombre.asc(), VaccineSchedule.dosis_numero.asc())
        .all()
    )

    out: list[ScheduleFullOut] = []
    for sch, vac in rows:
        out.append(ScheduleFullOut(
            schedule_id=sch.id,
            vaccine_id=vac.id,
            vaccine_nombre=vac.nombre,
            vaccine_descripcion=vac.descripcion,
            dosis_numero=sch.dosis_numero,
            edad_objetivo_meses=sch.edad_objetivo_meses,
            intervalo_min_dias=sch.intervalo_min_dias
        ))
    return out

@router.post("/schedule", response_model=ScheduleOut, dependencies=[Depends(require_roles(["ADMIN"]))])
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db)):
    vac = db.query(Vaccine).filter(Vaccine.id == payload.vaccine_id, Vaccine.activo == True).first()
    if not vac:
        raise HTTPException(status_code=400, detail="vaccine_id inválido")

    exists = db.query(VaccineSchedule).filter(
        VaccineSchedule.vaccine_id == payload.vaccine_id,
        VaccineSchedule.dosis_numero == payload.dosis_numero
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Ya existe esa dosis para esa vacuna")

    sch = VaccineSchedule(
        vaccine_id=payload.vaccine_id,
        dosis_numero=payload.dosis_numero,
        edad_objetivo_meses=payload.edad_objetivo_meses,
        intervalo_min_dias=payload.intervalo_min_dias
    )
    db.add(sch)
    db.commit()
    db.refresh(sch)
    return sch

@router.delete("/schedule/{schedule_id}", dependencies=[Depends(require_roles(["ADMIN"]))])
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    sch = db.query(VaccineSchedule).filter(VaccineSchedule.id == schedule_id).first()
    if not sch:
        raise HTTPException(status_code=404, detail="Esquema no encontrado")
    sch.activo = False
    db.commit()
    return {"ok": True}
