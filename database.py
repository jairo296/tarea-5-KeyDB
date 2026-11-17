
import redis
from config import Config


# CONEXION CON KEYDB

keydb = redis.Redis(
    host=Config.KEYDB_HOST,
    port=Config.KEYDB_PORT,
    password=Config.KEYDB_PASSWORD or None,
    db=Config.KEYDB_DB,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5
)


# COMPROBAR CONEXION

def comprobar_conexion():
    try:
        keydb.ping()
        print("Conexión con KeyDB exitosa.")
        return True

    except redis.RedisError as error:
        print(f"Error de conexión con KeyDB: {error}")
        return False
