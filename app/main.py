from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 👇 importa TODOS los routers que hayas creado
from .routers import (
    auth,
    personas,
    centro_salud,
    cargos_medicos,
    tipos_vacunas,
    historial_vacunacion,
    detalle_historial_vacuna,
    relacion_padre_hijo,
)

from .database import Base, engine

app = FastAPI(title="API Sistema de Vacunación - Avance 1")

# 👇 ORÍGENES PERMITIDOS (tu frontend React)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # permitir solo front local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 aquí registramos todas las rutas
app.include_router(auth.router)
app.include_router(personas.router)
app.include_router(centro_salud.router)
app.include_router(cargos_medicos.router)
app.include_router(tipos_vacunas.router)
app.include_router(historial_vacunacion.router)
app.include_router(detalle_historial_vacuna.router)
app.include_router(relacion_padre_hijo.router)


@app.get("/")
def root():
    return {"mensaje": "API de Vacunación funcionando"}
