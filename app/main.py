from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, personas
from .database import Base, engine

app = FastAPI(title="API Sistema de Vacunación - Avance 1")

# 👇 ORÍGENES PERMITIDOS (tu frontend)
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

app.include_router(auth.router)
app.include_router(personas.router)

@app.get("/")
def root():
    return {"mensaje": "API de Vacunación funcionando"}
