"""
Pipeline completo de ingesta: PDF -> texto -> chunks -> embeddings -> BD
"""
import os
import hashlib
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

from backend.db.connection import db_cursor
from backend.ingesta.extractor import extract_pdf
from backend.ingesta.chunker import chunk_document
from backend.ingesta.embedder import embed_batch

load_dotenv()


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()


def ingest_pdf(
    pdf_path: str,
    area_slug: str = "ops",
    titulo: str = None,
    autor: str = None,
    chunk_size: int = None,
    overlap: int = None
) -> Dict:
    chunk_size = chunk_size or int(os.getenv("CHUNK_SIZE", "500"))
    overlap = overlap or int(os.getenv("CHUNK_OVERLAP", "50"))
    
    print(f"\nIngesta de: {pdf_path}")
    print(f"   Area: {area_slug}")
    
    file_hash = file_sha256(pdf_path)
    print(f"   Hash: {file_hash[:16]}...")
    
    with db_cursor(dict_cursor=True) as cur:
        cur.execute("SELECT id, titulo FROM documents WHERE file_hash = %s", (file_hash,))
        existing = cur.fetchone()
        if existing:
            return {
                "status": "duplicate",
                "message": f"Documento ya existe (id={existing['id']})",
                "document_id": existing["id"]
            }
    
    print(f"   Extrayendo texto del PDF...")
    pdf_data = extract_pdf(pdf_path)
    print(f"      {pdf_data['page_count']} paginas, {pdf_data['total_chars']} caracteres")
    
    print(f"   Troceando en chunks (size={chunk_size}, overlap={overlap})...")
    chunks = chunk_document(pdf_data["pages"], chunk_size, overlap)
    print(f"      {len(chunks)} chunks generados")
    
    if not chunks:
        return {"status": "error", "message": "No se pudieron generar chunks"}
    
    print(f"   Generando embeddings...")
    texts = [c["content"] for c in chunks]
    embeddings = embed_batch(texts)
    print(f"      {len(embeddings)} embeddings (dim={len(embeddings[0])})")
    
    print(f"   Guardando en base de datos...")
    final_titulo = titulo or pdf_data["title"] or Path(pdf_path).stem
    final_autor = autor or pdf_data["author"] or "Desconocido"
    
    with db_cursor(dict_cursor=True) as cur:
        cur.execute("SELECT id FROM areas WHERE slug = %s", (area_slug,))
        area = cur.fetchone()
        if not area:
            return {"status": "error", "message": f"Area '{area_slug}' no existe"}
        area_id = area["id"]
        
        cur.execute("""
            INSERT INTO documents (area_id, titulo, filename, file_hash, file_path, page_count, autor, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo')
            RETURNING id
        """, (area_id, final_titulo, pdf_data["filename"], file_hash, str(pdf_path), pdf_data["page_count"], final_autor))
        doc_id = cur.fetchone()["id"]
        
        for chunk, embedding in zip(chunks, embeddings):
            cur.execute("""
                INSERT INTO chunks (document_id, chunk_index, content, page_number, embedding)
                VALUES (%s, %s, %s, %s, %s)
            """, (doc_id, chunk["chunk_index"], chunk["content"], chunk["page_number"], embedding))
    
    print(f"   Ingesta completada (document_id={doc_id})")
    
    return {
        "status": "ok",
        "document_id": doc_id,
        "titulo": final_titulo,
        "chunks": len(chunks),
        "pages": pdf_data["page_count"]
    }
