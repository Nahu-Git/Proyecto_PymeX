# db/connection.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Si ya tienes config.py con DB_PATH, puedes importar desde ahí:
# from config import DB_PATH
# Para que sea autocontenido, lo dejo definido aquí:
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "ispplus.db"


class DatabaseConnection:
    def __init__(self, db_path: str | Path = DB_PATH):
        self.db_path = str(db_path)

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            # Activar soporte de claves foráneas en SQLite
            conn.execute("PRAGMA foreign_keys = ON;")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


# Instancia global que usarán todos los repositorios
db = DatabaseConnection()
