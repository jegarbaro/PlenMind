"""
Chunker semantico - trocea texto respetando frases.
"""
import re
from typing import List, Dict


def split_into_sentences(text: str) -> List[str]:
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    sentences = split_into_sentences(text)
    if not sentences:
        return []
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        words = sentence.split()
        sentence_size = len(words)
        
        if current_size + sentence_size > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            overlap_words = " ".join(current_chunk).split()[-overlap:]
            current_chunk = [" ".join(overlap_words)]
            current_size = len(overlap_words)
        
        current_chunk.append(sentence)
        current_size += sentence_size
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


def chunk_document(pages: List[Dict], chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    all_chunks = []
    chunk_index = 0
    
    for page in pages:
        page_chunks = chunk_text(page["text"], chunk_size, overlap)
        for chunk_text_content in page_chunks:
            all_chunks.append({
                "chunk_index": chunk_index,
                "page_number": page["page_number"],
                "content": chunk_text_content,
                "char_count": len(chunk_text_content)
            })
            chunk_index += 1
    
    return all_chunks
