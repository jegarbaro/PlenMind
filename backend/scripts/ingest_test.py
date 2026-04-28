"""
Script de prueba para ingestar un PDF.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.ingesta.pipeline import ingest_pdf


def main():
    if len(sys.argv) < 2:
        print("Uso: python backend/scripts/ingest_test.py <ruta-al-pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    area_slug = sys.argv[2] if len(sys.argv) > 2 else "ops"
    
    result = ingest_pdf(pdf_path, area_slug=area_slug)
    
    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)
    for k, v in result.items():
        print(f"  {k}: {v}")
    print()


if __name__ == "__main__":
    main()
