#!/bin/bash
# Arranca la API de PlenMind en modo desarrollo (con auto-reload)
cd "$(dirname "$0")/../.." || exit 1
source venv/bin/activate
uvicorn backend.api.main:app --reload --port 8000 --host 127.0.0.1
