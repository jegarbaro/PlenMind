"""
Endpoints de gestion de documentos.
"""
import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from backend.db.connection import db_cursor
from backend.ingesta.pipeline import ingest_pdf

router = APIRouter()

UPLOADS_DIR = Path("docs")
UPLOADS_DIR.mkdir(exist_ok=True)


@router.get("")
def list_documents(area_slug: str = "ops"):
    """Lista todos los documentos activos de un area."""
    with db_cursor(dict_cursor=True) as cur:
        cur.execute("""
            SELECT 
                d.id, d.titulo, d.filename, d.page_count, d.autor, 
                d.version, d.status, d.created_at, d.file_path,
                a.slug as area_slug
            FROM documents d
            JOIN areas a ON d.area_id = a.id
            WHERE a.slug = %s AND d.status = 'activo'
            ORDER BY d.created_at DESC
        """, (area_slug,))
        docs = cur.fetchall()
    
    return {
        "area": area_slug,
        "total": len(docs),
        "documents": [dict(d) for d in docs]
    }


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    area_slug: str = Form("ops"),
    titulo: str = Form(None),
    autor: str = Form(None)
):
    """Sube un PDF y lo ingesta automaticamente en PlenMind."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF")
    
    # Guardar el archivo
    safe_filename = file.filename.replace(" ", "_")
    file_path = UPLOADS_DIR / safe_filename
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Ingesta
    try:
        result = ingest_pdf(
            str(file_path),
            area_slug=area_slug,
            titulo=titulo,
            autor=autor
        )
        return result
    except Exception as e:
        # Si falla la ingesta, borrar el archivo
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error en ingesta: {str(e)}")


@router.get("/{document_id}/download")
def download_document(document_id: int):
    """Descarga el PDF original de un documento."""
    with db_cursor(dict_cursor=True) as cur:
        cur.execute("""
            SELECT filename, file_path, titulo
            FROM documents
            WHERE id = %s
        """, (document_id,))
        doc = cur.fetchone()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    file_path = Path(doc["file_path"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo PDF no encontrado en disco")
    
    return FileResponse(
        path=file_path,
        filename=doc["filename"],
        media_type="application/pdf"
    )


@router.delete("/{document_id}")
def delete_document(document_id: int):
    """Marca un documento como obsoleto (soft delete)."""
    with db_cursor(dict_cursor=True) as cur:
        cur.execute("""
            UPDATE documents 
            SET status = 'obsoleto', updated_at = NOW() 
            WHERE id = %s
            RETURNING id, titulo
        """, (document_id,))
        result = cur.fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    return {"status": "ok", "message": f"Documento '{result['titulo']}' marcado como obsoleto"}
