import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env ubicado en la carpeta Backend
load_dotenv()

class Settings:
    def __init__(self) -> None:
        # URL de la base de datos
        self.database_url: str = os.getenv("DATABASE_URL", "")

        # JWT
        self.jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "cambia_esta_clave")
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")

        # Ojo: viene como string, lo convertimos a int con un valor por defecto
        self.access_token_expire_minutes: int = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
        )

settings = Settings()


