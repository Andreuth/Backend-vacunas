from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, users, children, vaccines, visits

app = FastAPI(title=settings.APP_NAME)

# CORS desde env
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# ✅ si en producción defines CORS_ORIGINS="https://xxx.vercel.app,https://yyy.vercel.app"
import os
cors_env = os.getenv("CORS_ORIGINS")
if cors_env:
    origins = [o.strip() for o in cors_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(children.router, prefix="/children", tags=["children"])
app.include_router(vaccines.router, prefix="/vaccines", tags=["vaccines"])
app.include_router(visits.router, prefix="/visits", tags=["visits"])

# ✅ opcional recomendado
@app.get("/health")
def health():
    return {"status": "ok"}
