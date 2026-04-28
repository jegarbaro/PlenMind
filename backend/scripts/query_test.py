"""
Script de prueba para hacer una consulta RAG completa.
Uso: python backend/scripts/query_test.py "tu pregunta aqui"
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.ingesta.search import search_chunks, format_context
from backend.providers.ollama_client import generate_response


def main():
    if len(sys.argv) < 2:
        print("Uso: python backend/scripts/query_test.py \"tu pregunta\"")
        print("Ejemplo: python backend/scripts/query_test.py \"Como reinicio un Fortinet?\"")
        sys.exit(1)
    
    pregunta = sys.argv[1]
    area_slug = sys.argv[2] if len(sys.argv) > 2 else "ops"
    
    print(f"\n{'='*60}")
    print(f"PREGUNTA: {pregunta}")
    print(f"AREA: {area_slug}")
    print(f"{'='*60}\n")
    
    # 1. Busqueda vectorial
    print("Buscando chunks relevantes...")
    t0 = time.time()
    chunks = search_chunks(pregunta, area_slug=area_slug, top_k=5)
    t_search = (time.time() - t0) * 1000
    print(f"   {len(chunks)} chunks encontrados en {t_search:.0f}ms\n")
    
    if not chunks:
        print("No se encontraron documentos relevantes para esta pregunta.")
        return
    
    print("FUENTES:")
    for i, c in enumerate(chunks, 1):
        print(f"  {i}. {c['document_titulo']} (pag. {c['page_number']}) - {c['similarity']:.1%} match")
    print()
    
    # 2. Formato de contexto
    contexto = format_context(chunks)
    
    # 3. Generacion con Ollama
    print("Generando respuesta con Llama 3.1...")
    t0 = time.time()
    result = generate_response(pregunta, contexto)
    t_gen = (time.time() - t0)
    
    print(f"\n{'='*60}")
    print("RESPUESTA")
    print(f"{'='*60}")
    print(result["respuesta"])
    print(f"\n{'='*60}")
    print("METRICAS")
    print(f"{'='*60}")
    print(f"  Tiempo busqueda: {t_search:.0f}ms")
    print(f"  Tiempo generacion: {t_gen:.1f}s")
    print(f"  Modelo: {result['modelo']}")
    print(f"  Tokens input: {result['tokens_input']}")
    print(f"  Tokens output: {result['tokens_output']}")
    print(f"  Coste: 0.00 EUR (modelo local)")
    print()


if __name__ == "__main__":
    main()
