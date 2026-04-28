#!/bin/bash
# PlenMind - Script de arranque
# Levanta backend (uvicorn) y frontend (vite) en background

set -e
cd "$(dirname "$0")"

ROOT="$(pwd)"
LOGS="$ROOT/logs"
mkdir -p "$LOGS"

echo "PlenMind - Arrancando servicios..."
echo "Directorio raiz: $ROOT"
echo ""

# Comprobar que no hay procesos previos
if lsof -ti:8000 > /dev/null 2>&1; then
  echo "  ! Puerto 8000 ocupado. Ejecuta ./stop.sh primero."
  exit 1
fi
if lsof -ti:5173 > /dev/null 2>&1; then
  echo "  ! Puerto 5173 ocupado. Ejecuta ./stop.sh primero."
  exit 1
fi

# Arrancar backend
echo "[1/2] Backend (uvicorn) en puerto 8000..."
source venv/bin/activate
nohup uvicorn backend.api.main:app --reload --port 8000 > "$LOGS/backend.log" 2>&1 &
echo $! > "$LOGS/backend.pid"
echo "      PID $(cat $LOGS/backend.pid) - log: logs/backend.log"

# Esperar a que el backend este listo
echo "      Esperando a que la API responda..."
for i in {1..20}; do
  if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "      OK - Backend listo"
    break
  fi
  sleep 1
done

# Arrancar frontend
echo ""
echo "[2/2] Frontend (vite) en puerto 5173..."
cd frontend-app
nohup npm run dev > "$ROOT/logs/frontend.log" 2>&1 &
echo $! > "$ROOT/logs/frontend.pid"
echo "      PID $(cat $ROOT/logs/frontend.pid) - log: logs/frontend.log"
cd "$ROOT"

# Esperar a que vite responda
sleep 3

echo ""
echo "PlenMind arrancado correctamente:"
echo "  - Frontend: http://localhost:5173"
echo "  - Backend:  http://localhost:8000/docs"
echo ""
echo "Para parar: ./stop.sh"
echo "Logs:       tail -f logs/backend.log  o  tail -f logs/frontend.log"
