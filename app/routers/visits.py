from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.deps_auth import require_roles, get_current_user
from app.models.user import User
from app.models.child import Child
from app.models.visit import Visit
from app.models.vaccine_schedule import VaccineSchedule
from app.models.vaccine_application import VaccineApplication
from app.models.vaccine import Vaccine  # ✅ agregado

from app.schemas.visit import (
    VisitCreate, VisitOut,
    VaccineApplicationCreate, VaccineApplicationOut,
    HistoryItem
)

from app.schemas.history_full import HistoryFullItem, AppliedVaccineFull  # ✅ agregado
from app.services.access import is_child_of_parent

router = APIRouter()

# ==========================
# Crear visita (ADMIN/PEDIATRA)
# ==========================
@router.post("/", response_model=VisitOut, dependencies=[Depends(require_roles(["ADMIN","PEDIATRA"]))])
def create_visit(payload: VisitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    child = db.query(Child).filter(Child.id == payload.child_id, Child.activo == True).first()
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")

    visit = Visit(
        child_id=payload.child_id,
        pediatrician_id=current_user.id,  # quien registra
        fecha_atencion=payload.fecha_atencion,
        peso_kg=payload.peso_kg,
        talla_cm=payload.talla_cm,
        observaciones=payload.observaciones
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit

# ==========================
# Listar visitas por niño
# ADMIN/PEDIATRA: pueden ver
# ==========================
@router.get("/by-child/{child_id}", response_model=list[VisitOut], dependencies=[Depends(require_roles(["ADMIN","PEDIATRA"]))])
def list_visits_by_child(child_id: int, db: Session = Depends(get_db)):
    return db.query(Visit).filter(Visit.child_id == child_id, Visit.activo == True).order_by(Visit.fecha_atencion.desc()).all()

# ==========================
# Aplicar vacuna a una visita
# ADMIN/PEDIATRA
# ==========================
@router.post("/{visit_id}/apply", response_model=VaccineApplicationOut, dependencies=[Depends(require_roles(["ADMIN","PEDIATRA"]))])
def apply_vaccine(visit_id: int, payload: VaccineApplicationCreate, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id, Visit.activo == True).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visita no encontrada")

    sch = db.query(VaccineSchedule).filter(VaccineSchedule.id == payload.schedule_id, VaccineSchedule.activo == True).first()
    if not sch:
        raise HTTPException(status_code=400, detail="schedule_id inválido")

    # Evitar duplicar dosis por niño (constraint uq_child_schedule_once ya ayuda)
    exists = db.query(VaccineApplication).filter(
        VaccineApplication.child_id == visit.child_id,
        VaccineApplication.schedule_id == payload.schedule_id,
        VaccineApplication.activo == True
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Esa dosis ya fue aplicada a este niño")

    app = VaccineApplication(
        visit_id=visit.id,
        child_id=visit.child_id,
        schedule_id=payload.schedule_id,
        fecha_aplicacion=payload.fecha_aplicacion,
        lote=payload.lote,
        proxima_fecha=payload.proxima_fecha
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

# ==========================
# HISTORIAL SIMPLE POR NIÑO
# ==========================
@router.get("/history/{child_id}", response_model=list[HistoryItem], dependencies=[Depends(require_roles(["ADMIN","PEDIATRA","REPRESENTANTE"]))])
def history(child_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Si es representante, validar pertenencia
    if current_user.rol == "REPRESENTANTE":
        if not is_child_of_parent(db, current_user.id, child_id):
            raise HTTPException(status_code=403, detail="No autorizado para ver este niño")

    child = db.query(Child).filter(Child.id == child_id, Child.activo == True).first()
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")

    visits = db.query(Visit).filter(
        Visit.child_id == child_id,
        Visit.activo == True
    ).order_by(Visit.fecha_atencion.desc()).all()

    result = []
    for v in visits:
        apps = db.query(VaccineApplication).filter(
            VaccineApplication.visit_id == v.id,
            VaccineApplication.activo == True
        ).order_by(VaccineApplication.fecha_aplicacion.desc()).all()

        result.append({"visit": v, "applications": apps})

    return result

# ==========================
# HISTORIAL FULL (con joins: schedule + vacuna)
# ADMIN/PEDIATRA: todo
# REPRESENTANTE: solo si es su hijo
# ==========================
@router.get(
    "/history/{child_id}/full",
    response_model=list[HistoryFullItem],
    dependencies=[Depends(require_roles(["ADMIN","PEDIATRA","REPRESENTANTE"]))],
)
def history_full(child_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Si es representante, validar pertenencia
    if current_user.rol == "REPRESENTANTE":
        if not is_child_of_parent(db, current_user.id, child_id):
            raise HTTPException(status_code=403, detail="No autorizado para ver este niño")

    child = db.query(Child).filter(Child.id == child_id, Child.activo == True).first()
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")

    visits = (
        db.query(Visit)
        .filter(Visit.child_id == child_id, Visit.activo == True)
        .order_by(Visit.fecha_atencion.desc())
        .all()
    )

    result: list[HistoryFullItem] = []

    for v in visits:
        rows = (
            db.query(VaccineApplication, VaccineSchedule, Vaccine)
            .join(VaccineSchedule, VaccineSchedule.id == VaccineApplication.schedule_id)
            .join(Vaccine, Vaccine.id == VaccineSchedule.vaccine_id)
            .filter(
                VaccineApplication.visit_id == v.id,
                VaccineApplication.activo == True,
                VaccineSchedule.activo == True,
                Vaccine.activo == True,
            )
            .order_by(VaccineApplication.fecha_aplicacion.desc())
            .all()
        )

        apps_full: list[AppliedVaccineFull] = []
        for app_row, sch, vac in rows:
            apps_full.append(
                AppliedVaccineFull(
                    application_id=app_row.id,
                    fecha_aplicacion=app_row.fecha_aplicacion,
                    lote=app_row.lote,
                    proxima_fecha=app_row.proxima_fecha,
                    schedule_id=sch.id,
                    dosis_numero=sch.dosis_numero,
                    edad_objetivo_meses=sch.edad_objetivo_meses,
                    vaccine_id=vac.id,
                    vaccine_nombre=vac.nombre,
                    vaccine_descripcion=vac.descripcion,
                )
            )

        result.append(HistoryFullItem(visit=v, applications=apps_full))

    return result
