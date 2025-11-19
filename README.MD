🧩 Sistema de Vacunación – BACKEND (FastAPI)

Este backend implementa una API REST para gestionar un sistema de vacunación.
Incluye autenticación con JWT, arquitectura por capas, conexión a PostgreSQL y migraciones con Alembic.

🚀 Tecnologías utilizadas

Python 3.10+

FastAPI

SQLAlchemy

PostgreSQL

Uvicorn

Alembic

JWT (python-jose)

Passlib (bcrypt)

python-multipart

📁 Estructura del proyecto
Backend/
│
├── app/
│   ├── core/          # Configuración global
│   ├── models/        # Modelos SQLAlchemy
│   ├── schemas/       # Pydantic Schemas
│   ├── services/      # Lógica de negocio
│   ├── security/      # JWT + hashing
│   ├── routers/       # Endpoints
│   ├── database.py    # Conexión DB
│   └── main.py        # Punto de entrada
│
├── alembic/           # Migraciones
├── alembic.ini
├── requirements.txt
└── .env

⚙️ Instalación
1️⃣ Crear entorno virtual
cd Backend
python -m venv venv
venv\Scripts\activate

2️⃣ Instalar dependencias
pip install -r requirements.txt

🔧 Configuración

Crear archivo .env en la carpeta Backend:

DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/vacunacion

JWT_SECRET_KEY=super_secreto
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60


⚠️ Cambiar TU_PASSWORD por tu contraseña real de PostgreSQL.

🗄️ Migraciones con Alembic
Inicializar BD

En PostgreSQL:

CREATE DATABASE vacunacion;

Ejecutar migraciones
alembic revision --autogenerate -m "init schema"
alembic upgrade head

▶️ Iniciar el servidor
uvicorn app.main:app --reload


Abrir navegador:

👉 http://127.0.0.1:8000/docs

(API interactiva Swagger)

🔐 Autenticación
POST /auth/login

Tipo: multipart/form-data

Campos:

username → número de documento

password → contraseña

Respuesta:

{
  "access_token": "eyJh...",
  "token_type": "bearer"
}


Luego usar el botón Authorize en Swagger.

📌 Entidad funcional requerida: PERSONAS
Endpoints:
Método	Endpoint	Descripción
POST	/personas/	Crear persona
GET	/personas/	Listar personas
GET	/personas/{id}	Obtener persona
PUT	/personas/{id}	Actualizar
DELETE	/personas/{id}	Desactivar
🛡️ Protección de rutas

Las rutas GET/PUT/DELETE requieren token:
Authorization: Bearer <token>

🧾 Estado del backend

✔ Base de datos completa
✔ JWT login
✔ CRUD Persona funcional
✔ Migraciones Alembic
✔ Arquitectura por capas
✔ Listo para consumo desde frontend

✍️ Autores / Grupo

(Coloca nombres, paralelo, profesor, fecha)

📘 FIN DEL README DEL BACKEND