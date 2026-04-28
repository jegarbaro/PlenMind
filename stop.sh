#!/bin/bash
# PlenMind - Script de parada

cd "$(dirname "$0")"
LOGS="logs"

echo "PlenMind - Deteniendo servicios..."

# Matar por PID si existen los archivos
for service in backend frontend; do
  PIDFILE="$LOGS/$service.pid"
  if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
      echo "  Matando $service (PID $PID)..."
      kill "$PID" 2>/dev/null || true
      sleep 1
      kill -9 "$PID" 2>/dev/null || true
    fi
    rm -f "$PIDFILE"
  fi
done

# Limpiar puertos por si acaso
for PORT in 8000 5173; do
  PIDS=$(lsof -ti:$PORT 2>/dev/null || true)
  if [ -n "$PIDS" ]; then
    echo "  Limpiando puerto $PORT..."
    echo "$PIDS" | xargs kill -9 2>/dev/null || true
  fi
done

echo "PlenMind detenido."
