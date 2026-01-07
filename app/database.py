from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .core.config import settings

# Engine de SQLAlchemy usando la URL del .env
engine = create_engine(settings.database_url, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependencia para FastAPI (inyectar la sesión en los endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
