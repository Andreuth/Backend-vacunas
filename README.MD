Backend SISCONI (FastAPI)

SISCONI Backend es la API REST del sistema de control de vacunación infantil.
Gestiona autenticación, usuarios, niños, vacunas, esquemas de dosis y visitas médicas.

🛠 Tecnologías

Python 3.10+

FastAPI

Uvicorn

SQLAlchemy

Alembic

PostgreSQL

📌 Endpoints útiles

Documentación Swagger:
http://localhost:8000/docs

Health check (si está habilitado):
http://localhost:8000/health

🔐 Variables de entorno

Crear un archivo .env en la carpeta backend/:

ENV=dev
SECRET_KEY=tu_clave_secreta_larga
ACCESS_TOKEN_EXPIRE_MINUTES=120

DB_HOST=db
DB_PORT=5432
DB_NAME=sisconi
DB_USER=sisconi_user
DB_PASSWORD=sisconi_pass

CORS_ORIGINS=https://frontend-vacunacion.vercel.app

🚧 1. Desarrollo con Docker (Tema 4.2)

Desde la raíz del proyecto:

docker compose up -d --build
docker compose ps
docker compose logs -f backend

Backend disponible en:
http://localhost:8000

💻 2. Desarrollo local sin Docker
Crear entorno virtual

cd backend
python -m venv venv

Linux / Mac:
source venv/bin/activate

Windows (PowerShell):
.\venv\Scripts\Activate.ps1

Instalar dependencias

pip install -r requirements.txt

Ejecutar migraciones

alembic upgrade head

Levantar servidor

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

🚀 3. Producción (Ubuntu Server – SIN Docker)

El backend se despliega en una máquina virtual con Ubuntu Server.

Servicio systemd

Archivo: /etc/systemd/system/sisconi.service

[Unit]
Description=SISCONI FastAPI
After=network.target postgresql.service

[Service]
User=sisconi
WorkingDirectory=/home/sisconi/sisconi/backend
EnvironmentFile=/home/sisconi/sisconi/backend/.env
ExecStart=/home/sisconi/sisconi/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

Activar servicio:

sudo systemctl daemon-reload
sudo systemctl enable sisconi
sudo systemctl restart sisconi
sudo systemctl status sisconi

🌐 Publicación en Internet

Frontend desplegado en Vercel

Backend en Ubuntu Server

Dominio público expuesto mediante Cloudflare Tunnel

Ejemplo:
https://back-sisconi.com

📸 Evidencias sugeridas

systemctl status sisconi

ufw status

Backend accesible desde dominio

👥 Autores

Grupo F SISCONI – Aplicaciones Web II