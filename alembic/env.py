import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- AÑADIDO: hacer que Python pueda encontrar el paquete "app" ---
# Alembic se ejecuta desde la carpeta "Backend", y "env.py" está en "Backend/alembic".
# Con esto añadimos "Backend" al sys.path, para poder hacer "from app...." sin errores.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos configuración y Base desde nuestra app
from app.core.config import settings
from app.database import Base
# 👇 Esto fuerza la carga de TODOS los modelos (Persona, CentroSalud, etc.)
from app import models  # noqa: F401

# -----------------------------------------------------------------

# Objeto de configuración de Alembic (lee alembic.ini)
config = context.config

# Opcional: setear la URL de la BD desde settings (en vez de solo alembic.ini)
if settings.database_url:
    config.set_main_option("sqlalchemy.url", settings.database_url)

# Configurar logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aquí va la metadata de nuestros modelos
# Esto permite que 'alembic revision --autogenerate' detecte las tablas
target_metadata = Base.metadata

# Puedes obtener otras opciones de config si las necesitas:
# my_important_option = config.get_main_option("my_important_option")
# ...


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
