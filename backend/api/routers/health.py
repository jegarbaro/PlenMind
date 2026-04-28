"""
Endpoint de health check.
"""
from fastapi import APIRouter
from backend.db.connection import db_cursor

router = APIRouter()


@router.get("/health")
def health_check():
    """Verifica que la API y la BD estan funcionando."""
    try:
        with db_cursor(dict_cursor=True) as cur:
            cur.execute("SELECT count(*) as total FROM areas;")
            areas_count = cur.fetchone()["total"]
            cur.execute("SELECT count(*) as total FROM documents WHERE status='activo';")
            docs_count = cur.fetchone()["total"]
            cur.execute("SELECT count(*) as total FROM chunks;")
            chunks_count = cur.fetchone()["total"]
        
        return {
            "status": "healthy",
            "database": "ok",
            "stats": {
                "areas": areas_count,
                "documents_active": docs_count,
                "chunks_total": chunks_count
            }
        }
    except Exception as e:
        return {"status": "unhealthy", "database": "error", "message": str(e)}
