#!/bin/bash

# stop.sh - Script para detener y limpiar Textual Guardian
# Uso: ./stop.sh

set -e  # Salir si algún comando falla

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
IMAGE_NAME="textual-guardian"
CONTAINER_NAME="textual-guardian-app"

echo -e "${BLUE}🛑 Deteniendo Textual Guardian...${NC}"
echo ""

# 1. Detener contenedor
echo -e "${YELLOW}⏹️  Deteniendo contenedor...${NC}"
if podman stop $CONTAINER_NAME 2>/dev/null; then
    echo -e "${GREEN}✅ Contenedor detenido${NC}"
else
    echo -e "${BLUE}ℹ️  No hay contenedor ejecutándose${NC}"
fi

# 2. Eliminar contenedor
echo -e "${YELLOW}🗑️  Eliminando contenedor...${NC}"
if podman rm $CONTAINER_NAME 2>/dev/null; then
    echo -e "${GREEN}✅ Contenedor eliminado${NC}"
else
    echo -e "${BLUE}ℹ️  No hay contenedor que eliminar${NC}"
fi

echo ""

# Preguntar si quiere eliminar la imagen también
read -p "¿Quieres eliminar también la imagen Docker? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🗑️  Eliminando imagen...${NC}"
    if podman rmi $IMAGE_NAME 2>/dev/null; then
        echo -e "${GREEN}✅ Imagen eliminada${NC}"
    else
        echo -e "${BLUE}ℹ️  No hay imagen que eliminar${NC}"
    fi
fi

echo ""
echo -e "${GREEN}🎉 ¡Textual Guardian detenido y limpio!${NC}"
echo -e "${BLUE}💡 Para volver a iniciar usa: ${GREEN}./start.sh${NC}"
