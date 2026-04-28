"""
Cliente para Ollama (modelo de generacion local).
"""
import os
import ollama
from dotenv import load_dotenv

load_dotenv()


def generate_response(
    pregunta: str,
    contexto: str,
    modelo: str = None,
    temperatura: float = 0.3
) -> dict:
    """
    Genera una respuesta usando Llama 3.1 con contexto del RAG.
    Devuelve dict con respuesta y metadata.
    """
    modelo = modelo or os.getenv("OLLAMA_MODEL_GEN", "llama3.1:8b")
    
    system_prompt = """Eres PlenMind, el asistente de IA interno de Plenergy para documentacion IT.
Tu funcion es responder preguntas tecnicas usando EXCLUSIVAMENTE el contexto proporcionado de los documentos internos.

REGLAS CRITICAS:
1. Si la respuesta no esta en el contexto, di claramente: "No encuentro esa informacion en la documentacion disponible."
2. NUNCA inventes informacion ni uses conocimiento general.
3. Cita las paginas y secciones de donde sacas la informacion (ej. "segun pag. 5, seccion 6.2").
4. Responde en el mismo idioma de la pregunta (espanol por defecto).
5. Se conciso pero completo: maximo 5 parrafos.
6. Si la pregunta es ambigua, pide aclaracion antes de responder."""
    
    user_prompt = f"""CONTEXTO DE LA DOCUMENTACION:
{contexto}

PREGUNTA DEL USUARIO:
{pregunta}

RESPUESTA:"""
    
    response = ollama.chat(
        model=modelo,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        options={"temperature": temperatura}
    )
    
    return {
        "respuesta": response["message"]["content"],
        "modelo": modelo,
        "proveedor": "ollama",
        "tokens_input": response.get("prompt_eval_count", 0),
        "tokens_output": response.get("eval_count", 0),
        "duracion_ms": int(response.get("total_duration", 0) / 1_000_000)
    }
