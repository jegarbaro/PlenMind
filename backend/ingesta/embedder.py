"""
Generador de embeddings usando sentence-transformers.
"""
import os
from typing import List
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
        print(f"  Cargando modelo de embeddings: {model_name}")
        _model = SentenceTransformer(model_name)
        print(f"  Modelo cargado. Dimension: {_model.get_sentence_embedding_dimension()}")
    return _model


def embed_text(text: str) -> List[float]:
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
    return embedding.tolist()


def embed_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    model = get_model()
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        show_progress_bar=True
    )
    return embeddings.tolist()
