import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()


class Config:

    # Configuración de Flask
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError("No se encontró SECRET_KEY en el archivo .env")

    DEBUG = False

    # Configuración de KeyDB
    KEYDB_HOST = os.getenv("KEYDB_HOST", "localhost")
    KEYDB_PORT = int(os.getenv("KEYDB_PORT", 6379))
    KEYDB_PASSWORD = os.getenv("KEYDB_PASSWORD")
    KEYDB_DB = int(os.getenv("KEYDB_DB", 0))

    # Configuración de imágenes
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
