"""
Busqueda vectorial en pgvector.
"""
from typing import List, Dict
from backend.db.connection import db_cursor
from backend.ingesta.embedder import embed_text


def search_chunks(
    pregunta: str,
    area_slug: str = "ops",
    top_k: int = 5,
    min_similarity: float = 0.3
) -> List[Dict]:
    """
    Busca los top_k chunks mas similares a la pregunta.
    Solo busca en documentos activos del area indicada.
    Devuelve lista con chunks ordenados por similitud descendente.
    """
    query_embedding = embed_text(pregunta)
    
    with db_cursor(dict_cursor=True) as cur:
        cur.execute("""
            SELECT 
                c.id as chunk_id,
                c.content,
                c.page_number,
                c.section,
                d.id as document_id,
                d.titulo as document_titulo,
                d.filename,
                1 - (c.embedding <=> %s::vector) as similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            JOIN areas a ON d.area_id = a.id
            WHERE 
                d.status = 'activo'
                AND a.slug = %s
                AND 1 - (c.embedding <=> %s::vector) > %s
            ORDER BY c.embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, area_slug, query_embedding, min_similarity, query_embedding, top_k))
        
        results = cur.fetchall()
    
    return [dict(r) for r in results]


def format_context(chunks: List[Dict]) -> str:
    """Formatea los chunks como contexto para el LLM."""
    if not chunks:
        return "No se encontraron documentos relevantes."
    
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"--- Fragmento {i} ---")
        lines.append(f"Documento: {chunk['document_titulo']}")
        lines.append(f"Pagina: {chunk['page_number']}")
        lines.append(f"Similitud: {chunk['similarity']:.2%}")
        lines.append(f"Contenido: {chunk['content']}")
        lines.append("")
    
    return "\n".join(lines)
