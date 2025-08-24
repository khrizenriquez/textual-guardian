# 📝 Textual Guardian

Analizador de redacción académica desarrollado en Python con Streamlit que detecta problemas comunes en textos académicos.

## ✨ Características

- 🔄 **Detección de palabras repetidas** - Identifica términos que se repiten excesivamente
- 📋 **Detección de participios** - Encuentra palabras terminadas en -ado, -ido  
- 🔄 **Detección de gerundios** - Localiza palabras terminadas en -ando, -endo
- ⚠️ **Expresiones problemáticas** - Detecta frases como "ya que", "etc.", "pero"
- 🏷️ **Adjetivos calificativos** - Identifica adjetivos vagos como "grande", "pequeño"
- ✏️ **Puntuación incorrecta** - Encuentra comas antes del conectivo "y"
- 📊 **Estadísticas del texto** - Conteo de palabras y resumen de problemas

## 🚀 Instalación y Uso

### Requisitos previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. Clona este repositorio:
```bash
git clone <repository-url>
cd textual-guardian
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Ejecución

Ejecuta la aplicación con:
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🐳 Uso con Podman

### Requisitos previos para Podman
- Podman instalado en tu sistema
- podman-compose (opcional, para usar docker-compose.yml)

### Opción 1: Usando Makefile (Recomendado)

El proyecto incluye un `Makefile` para facilitar el uso con Podman:

```bash
# Ver todos los comandos disponibles
make help

# Construir la imagen
make build

# Ejecutar el contenedor
make run

# Ver logs
make logs

# Detener y limpiar
make clean
```

### Opción 2: Comandos manuales de Podman

```bash
# Construir la imagen
podman build -t textual-guardian .

# Ejecutar el contenedor
podman run -d --name textual-guardian-app -p 8501:8501 textual-guardian

# Ver logs
podman logs -f textual-guardian-app

# Detener el contenedor
podman stop textual-guardian-app

# Eliminar el contenedor
podman rm textual-guardian-app
```

### Opción 3: Usando podman-compose

```bash
# Levantar la aplicación
podman-compose up -d

# Ver logs
podman-compose logs -f

# Detener la aplicación
podman-compose down
```

### Modo Desarrollo

Para desarrollo con recarga automática:

```bash
# Usando Makefile
make dev

# O manualmente
podman run -d --name textual-guardian-dev -p 8501:8501 -v ./:/app:Z textual-guardian
```

**Acceso:** La aplicación estará disponible en `http://localhost:8501`

## 📖 Cómo usar

1. Abre la aplicación en tu navegador
2. Pega o escribe tu texto en el área de texto
3. Haz clic en "🔍 Analizar Texto"
4. Revisa los resultados y sugerencias de mejora

## 🎯 Reglas de Redacción Implementadas

La aplicación detecta problemas basados en las siguientes indicaciones académicas:

1. **Repetición de términos** - Sugiere usar sinónimos
2. **Participios** - Evitar terminaciones -ado, -ido
3. **Gerundios** - Eliminar terminaciones -ando, -endo
4. **Expresiones prohibidas**:
   - "ya que" → usar "debido a que", "dado que"
   - "etc." → usar "tales como", "entre otros"
   - "pero" → usar "sin embargo", "no obstante"
   - "puede/pueden" → usar "permite", "facilita"
   - "pretende" → usar "busca", "requiere"
5. **Adjetivos calificativos** - Evitar términos vagos
6. **Puntuación** - No usar coma antes de "y"

## 🛠️ Estructura del Proyecto

```
textual-guardian/
├── app.py              # Aplicación principal de Streamlit
├── text_analyzer.py    # Módulo de análisis de texto
├── requirements.txt    # Dependencias de Python
├── Dockerfile          # Configuración de contenedor
├── docker-compose.yml  # Configuración para podman-compose
├── Makefile           # Comandos automatizados para Podman
├── .dockerignore      # Archivos ignorados en la imagen
├── README.md          # Este archivo
└── LICENSE           # Licencia del proyecto
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo `LICENSE`.
