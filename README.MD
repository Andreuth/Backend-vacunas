SISCONI – Backend

Backend del sistema SISCONI (Sistema de Control de Vacunación Infantil), desarrollado con FastAPI y PostgreSQL.

Permite la gestión de:
- Usuarios (ADMIN, PEDIATRA, REPRESENTANTE)
- Niños y representantes
- Visitas médicas (peso, talla)
- Vacunas y esquema por dosis
- Historial de vacunación
- Próximas vacunas automáticas

TECNOLOGÍAS
- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT

INSTALACIÓN
1. Crear entorno virtual
   python -m venv venv

2. Activar entorno
   Windows: venv\Scripts\activate
   Linux/Mac: source venv/bin/activate

3. Instalar dependencias
   pip install -r requirements.txt

CONFIGURACIÓN
Crear archivo .env con:
DATABASE_URL=postgresql://usuario:password@localhost:5432/sisconi_db
SECRET_KEY=supersecreto
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

EJECUCIÓN
uvicorn app.main:app --reload

DOCUMENTACIÓN
http://127.0.0.1:8000/docs

ROLES
ADMIN: administra usuarios y vacunas
PEDIATRA: registra niños, visitas y vacunas
REPRESENTANTE: consulta historial

NOTA
El administrador no puede cambiar roles, solo editar datos básicos.

