"""
Inicializa la base de datos PlenMind ejecutando schema.sql
Uso: python backend/scripts/init_db.py
"""
import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def main():
    schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
    
    if not schema_path.exists():
        print(f"❌ No encuentro schema.sql en {schema_path}")
        return
    
    print(f"📄 Leyendo {schema_path}")
    with open(schema_path, 'r') as f:
        sql = f.read()
    
    print(f"🔌 Conectando a {os.getenv('DB_NAME')} en {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "plenmind"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "") or None
    )
    
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema='public';")
        tables = cur.fetchone()[0]
        cur.execute("SELECT slug, nombre, activa FROM areas;")
        areas = cur.fetchall()
    
    conn.close()
    
    print(f"\n✅ Esquema aplicado correctamente")
    print(f"   Tablas creadas: {tables}")
    print(f"   Áreas:")
    for slug, nombre, activa in areas:
        estado = "✅ activa" if activa else "⏸  inactiva"
        print(f"     - {nombre} ({slug}) {estado}")

if __name__ == "__main__":
    main()
