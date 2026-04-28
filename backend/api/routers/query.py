"""
Endpoint de consulta RAG (busqueda + generacion).
"""
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from backend.ingesta.search import search_chunks, format_context
from backend.providers.ollama_client import generate_response
from backend.db.connection import db_cursor

router = APIRouter()


class QueryRequest(BaseModel):
    pregunta: str = Field(..., min_length=3, description="Pregunta del usuario")
    area_slug: str = Field("ops", description="Area en la que buscar (ops/infra/legal)")
    top_k: int = Field(5, ge=1, le=20, description="Numero de chunks a recuperar")
    temperatura: float = Field(0.3, ge=0.0, le=1.0, description="Temperatura del modelo")


class FuenteCitada(BaseModel):
    document_id: int
    document_titulo: str
    page_number: int
    similarity: float
    filename: str


class QueryResponse(BaseModel):
    pregunta: str
    respuesta: str
    fuentes: list[FuenteCitada]
    metricas: dict


@router.post("", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    """
    Consulta RAG completa: busca chunks relevantes y genera respuesta con LLM.
    """
    # 1. Busqueda vectorial
    t0 = time.time()
    chunks = search_chunks(
        request.pregunta,
        area_slug=request.area_slug,
        top_k=request.top_k
    )
    t_search = (time.time() - t0) * 1000
    
    if not chunks:
        return QueryResponse(
            pregunta=request.pregunta,
            respuesta="No encuentro informacion relevante en la documentacion para responder a tu pregunta.",
            fuentes=[],
            metricas={
                "tiempo_busqueda_ms": int(t_search),
                "tiempo_generacion_ms": 0,
                "chunks_encontrados": 0,
                "proveedor": "ninguno",
                "modelo": "ninguno",
                "tokens_input": 0,
                "tokens_output": 0,
                "coste_eur": 0.0
            }
        )
    
    # 2. Formato de contexto
    contexto = format_context(chunks)
    
    # 3. Generacion
    t0 = time.time()
    result = generate_response(
        request.pregunta,
        contexto,
        temperatura=request.temperatura
    )
    t_gen = (time.time() - t0) * 1000
    
    # 4. Guardar consulta en historico
    try:
        with db_cursor(dict_cursor=True) as cur:
            cur.execute("SELECT id FROM areas WHERE slug = %s", (request.area_slug,))
            area = cur.fetchone()
            area_id = area["id"] if area else None
            
            cur.execute("""
                INSERT INTO consultas (
                    area_id, pregunta, respuesta, chunks_usados,
                    proveedor, modelo, tokens_input, tokens_output, duracion_ms
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                area_id,
                request.pregunta,
                result["respuesta"],
                [c["chunk_id"] for c in chunks],
                result["proveedor"],
                result["modelo"],
                result["tokens_input"],
                result["tokens_output"],
                int(t_gen)
            ))
    except Exception as e:
        print(f"Warning: no se pudo guardar consulta en historico: {e}")
    
    # 5. Respuesta
    fuentes = [
        FuenteCitada(
            document_id=c["document_id"],
            document_titulo=c["document_titulo"],
            page_number=c["page_number"],
            similarity=round(c["similarity"], 4),
            filename=c["filename"]
        )
        for c in chunks
    ]
    
    return QueryResponse(
        pregunta=request.pregunta,
        respuesta=result["respuesta"],
        fuentes=fuentes,
        metricas={
            "tiempo_busqueda_ms": int(t_search),
            "tiempo_generacion_ms": int(t_gen),
            "chunks_encontrados": len(chunks),
            "proveedor": result["proveedor"],
            "modelo": result["modelo"],
            "tokens_input": result["tokens_input"],
            "tokens_output": result["tokens_output"],
            "coste_eur": 0.0
        }
    )
