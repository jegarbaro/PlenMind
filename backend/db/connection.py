"""
Helpers para conexion a PostgreSQL.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Devuelve una conexion nueva a PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "plenmind"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "") or None
    )


@contextmanager
def db_cursor(dict_cursor=False):
    """
    Context manager que abre conexion, da cursor y hace commit/close automatico.
    Uso:
        with db_cursor() as cur:
            cur.execute("SELECT ...")
    """
    conn = get_connection()
    try:
        cursor_factory = RealDictCursor if dict_cursor else None
        cur = conn.cursor(cursor_factory=cursor_factory)
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
