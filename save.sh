#!/bin/bash
# PlenMind - Script para guardar cambios en GitHub
# Uso: ./save.sh "mensaje del commit"
# Si no se pasa mensaje, usa uno por defecto con la fecha

set -e
cd "$(dirname "$0")"

# Comprobar que estamos en un repo git
if [ ! -d ".git" ]; then
  echo "Error: este directorio no es un repositorio git."
  exit 1
fi

# Mensaje del commit
if [ -z "$1" ]; then
  MENSAJE="Update $(date '+%Y-%m-%d %H:%M')"
  echo "Sin mensaje proporcionado. Usando: $MENSAJE"
else
  MENSAJE="$1"
fi

echo ""
echo "PlenMind - Guardando cambios en GitHub..."
echo ""

# Mostrar estado actual
echo "[1/4] Estado del repositorio:"
git status --short
echo ""

# Comprobar si hay cambios
if [ -z "$(git status --porcelain)" ]; then
  echo "No hay cambios para guardar."
  exit 0
fi

# Anadir todos los cambios
echo "[2/4] Anadiendo cambios..."
git add -A

# Crear commit
echo "[3/4] Creando commit: \"$MENSAJE\""
git commit -m "$MENSAJE"

# Push a remoto
echo "[4/4] Subiendo a GitHub..."
RAMA=$(git branch --show-current)
git push origin "$RAMA"

echo ""
echo "Cambios guardados correctamente en la rama $RAMA."
echo "Repositorio: $(git config --get remote.origin.url)"
