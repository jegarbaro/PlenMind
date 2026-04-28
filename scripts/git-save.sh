#!/bin/bash

# ╔══════════════════════════════════════════════════════════════╗
# ║  PlenMind - Script de guardado en GitHub                     ║
# ║  Uso: ./scripts/git-save.sh "mensaje del commit"             ║
# ╚══════════════════════════════════════════════════════════════╝

# Colores
BLUE='\033[0;34m'
ORANGE='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  ${ORANGE}PlenMind${NC} - Guardado automatico en GitHub                  ${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Ir a la raiz del proyecto
cd "$(dirname "$0")/.." || exit 1

# Verificar que estamos en un repo git
if [ ! -d .git ]; then
    echo -e "${RED}❌ Esta carpeta no es un repositorio git${NC}"
    exit 1
fi

# Mensaje del commit
if [ -z "$1" ]; then
    echo -e "${ORANGE}⚠  No has dado un mensaje de commit${NC}"
    echo -e "${GRAY}   Escribe uno corto describiendo los cambios:${NC}"
    read -r COMMIT_MSG
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="chore: actualizacion automatica $(date '+%d-%m-%Y %H:%M')"
        echo -e "${GRAY}   Usando mensaje por defecto: ${COMMIT_MSG}${NC}"
    fi
else
    COMMIT_MSG="$1"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}1️⃣  Revisando cambios...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
    echo -e "${GREEN}✅ No hay cambios para guardar${NC}"
    echo -e "${GRAY}   El repositorio esta al dia${NC}"
    echo ""
    exit 0
fi

git status --short
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}2️⃣  Anadiendo todos los cambios...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
git add .
echo -e "${GREEN}✅ Anadidos${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}3️⃣  Creando punto de guardado...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GRAY}   Mensaje: ${COMMIT_MSG}${NC}"
git commit -m "$COMMIT_MSG"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}4️⃣  Subiendo a GitHub...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
git push

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅  Cambios guardados correctamente en GitHub                ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GRAY}   Repositorio: https://github.com/jegarbaro/PlenMind${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Error al subir a GitHub${NC}"
    echo -e "${GRAY}   Revisa tu conexion o credenciales${NC}"
    exit 1
fi
