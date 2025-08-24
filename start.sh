#!/bin/bash

# start.sh - Script para reiniciar Textual Guardian con Podman
# Uso: ./start.sh

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
PORT="8501"

echo -e "${BLUE}🚀 Iniciando Textual Guardian...${NC}"
echo ""

# Función para mostrar spinner
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# 1. Detener y eliminar contenedor existente
echo -e "${YELLOW}🛑 Deteniendo contenedor existente...${NC}"
if podman stop $CONTAINER_NAME 2>/dev/null; then
    echo -e "${GREEN}✅ Contenedor detenido${NC}"
else
    echo -e "${BLUE}ℹ️  No hay contenedor ejecutándose${NC}"
fi

echo -e "${YELLOW}🗑️  Eliminando contenedor...${NC}"
if podman rm $CONTAINER_NAME 2>/dev/null; then
    echo -e "${GREEN}✅ Contenedor eliminado${NC}"
else
    echo -e "${BLUE}ℹ️  No hay contenedor que eliminar${NC}"
fi

echo ""

# 2. Construir imagen
echo -e "${YELLOW}🔨 Construyendo imagen...${NC}"
if podman build -t $IMAGE_NAME . --quiet; then
    echo -e "${GREEN}✅ Imagen construida exitosamente${NC}"
else
    echo -e "${RED}❌ Error al construir la imagen${NC}"
    exit 1
fi

echo ""

# 3. Ejecutar contenedor
echo -e "${YELLOW}🏃 Ejecutando contenedor...${NC}"
if podman run -d --name $CONTAINER_NAME -p $PORT:$PORT $IMAGE_NAME; then
    echo -e "${GREEN}✅ Contenedor iniciado exitosamente${NC}"
else
    echo -e "${RED}❌ Error al iniciar el contenedor${NC}"
    exit 1
fi

echo ""

# 4. Verificar estado
echo -e "${YELLOW}🔍 Verificando estado...${NC}"
sleep 2

if podman ps --filter name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}" | grep -q $CONTAINER_NAME; then
    echo -e "${GREEN}✅ Contenedor ejecutándose correctamente${NC}"
    echo ""
    echo -e "${GREEN}🎉 ¡Textual Guardian está listo!${NC}"
    echo -e "${BLUE}📱 Accede a la aplicación en: ${GREEN}http://localhost:$PORT${NC}"
    echo ""
    echo -e "${YELLOW}💡 Comandos útiles:${NC}"
    echo -e "   Ver logs:    ${BLUE}podman logs -f $CONTAINER_NAME${NC}"
    echo -e "   Detener:     ${BLUE}podman stop $CONTAINER_NAME${NC}"
    echo -e "   Shell:       ${BLUE}podman exec -it $CONTAINER_NAME /bin/bash${NC}"
    echo -e "   Estado:      ${BLUE}make status${NC}"
    echo ""
else
    echo -e "${RED}❌ El contenedor no se está ejecutando correctamente${NC}"
    echo -e "${YELLOW}📋 Logs del contenedor:${NC}"
    podman logs $CONTAINER_NAME
    exit 1
fi
