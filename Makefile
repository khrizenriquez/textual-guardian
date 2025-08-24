# Makefile para facilitar comandos de Podman

# Variables
IMAGE_NAME = textual-guardian
CONTAINER_NAME = textual-guardian-app
PORT = 8501

# Colores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
NC = \033[0m # No Color

.PHONY: help build run stop clean logs shell quick-start quick-stop

help: ## Mostrar ayuda
	@echo "$(GREEN)Textual Guardian - Comandos disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

build: ## Construir la imagen con Podman
	@echo "$(GREEN)Construyendo imagen con Podman...$(NC)"
	podman build -t $(IMAGE_NAME) .

run: ## Ejecutar el contenedor
	@echo "$(GREEN)Iniciando contenedor...$(NC)"
	podman run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		$(IMAGE_NAME)
	@echo "$(GREEN)Aplicación disponible en: http://localhost:$(PORT)$(NC)"

compose-up: ## Levantar con podman-compose
	@echo "$(GREEN)Iniciando con podman-compose...$(NC)"
	podman-compose up -d
	@echo "$(GREEN)Aplicación disponible en: http://localhost:$(PORT)$(NC)"

compose-down: ## Detener con podman-compose
	@echo "$(YELLOW)Deteniendo contenedores...$(NC)"
	podman-compose down

stop: ## Detener el contenedor
	@echo "$(YELLOW)Deteniendo contenedor...$(NC)"
	podman stop $(CONTAINER_NAME) || true

remove: ## Eliminar el contenedor
	@echo "$(RED)Eliminando contenedor...$(NC)"
	podman rm $(CONTAINER_NAME) || true

clean: stop remove ## Limpiar contenedores e imágenes
	@echo "$(RED)Limpiando imágenes...$(NC)"
	podman rmi $(IMAGE_NAME) || true

logs: ## Ver logs del contenedor
	podman logs -f $(CONTAINER_NAME)

shell: ## Abrir shell en el contenedor
	podman exec -it $(CONTAINER_NAME) /bin/bash

status: ## Ver estado del contenedor
	@echo "$(GREEN)Estado del contenedor:$(NC)"
	podman ps -a --filter name=$(CONTAINER_NAME)

dev: ## Modo desarrollo con volumen montado
	@echo "$(GREEN)Iniciando en modo desarrollo...$(NC)"
	podman run -d \
		--name $(CONTAINER_NAME)-dev \
		-p $(PORT):$(PORT) \
		-v ./:/app:Z \
		$(IMAGE_NAME)
	@echo "$(GREEN)Modo desarrollo activo en: http://localhost:$(PORT)$(NC)"

quick-start: ## Reinicio completo con un solo comando (usando start.sh)
	@echo "$(GREEN)Ejecutando reinicio completo...$(NC)"
	./start.sh

quick-stop: ## Detener y limpiar completamente (usando stop.sh)
	@echo "$(YELLOW)Deteniendo y limpiando...$(NC)"
	./stop.sh
