"""
Extractor de texto de PDFs usando PyMuPDF.
"""
import fitz
from pathlib import Path
from typing import Dict


def extract_pdf(pdf_path: str) -> Dict:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF no encontrado: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            pages.append({
                "page_number": i,
                "text": text,
                "char_count": len(text)
            })
    
    metadata = doc.metadata or {}
    
    result = {
        "filename": pdf_path.name,
        "page_count": doc.page_count,
        "title": metadata.get("title", "") or pdf_path.stem,
        "author": metadata.get("author", ""),
        "pages": pages,
        "total_chars": sum(p["char_count"] for p in pages)
    }
    
    doc.close()
    return result
