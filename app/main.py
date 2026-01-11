from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, users, children, vaccines, visits

app = FastAPI(title=settings.APP_NAME)

# ======================
# CORS
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Routers
# ======================
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(children.router, prefix="/children", tags=["children"])
app.include_router(vaccines.router, prefix="/vaccines", tags=["vaccines"])
app.include_router(visits.router, prefix="/visits", tags=["visits"])
