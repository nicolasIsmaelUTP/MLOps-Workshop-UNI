# ============================================================
# Makefile — Taller MLOps UNI
# ============================================================
# Comandos rápidos para las tareas más comunes del proyecto.
#
# Uso:
#   make setup     → Crear entorno virtual e instalar dependencias
#   make train     → Entrenar el modelo
#   make predict   → Hacer una predicción de prueba
#   make api       → Levantar la API localmente
#   make docker    → Construir la imagen Docker
#   make run       → Ejecutar el contenedor Docker
# ============================================================

.PHONY: setup train predict api docker run clean help

# Variables
PYTHON = python
VENV = venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python

# --- Configuración del entorno ---

setup:  ## Crear entorno virtual e instalar dependencias
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Entorno listo. Activa con: source venv/bin/activate"

# --- Entrenamiento y predicción ---

train:  ## Entrenar el modelo y exportar con joblib
	$(PYTHON) src/train.py --config configs/params.yaml

predict:  ## Hacer una predicción de prueba con el modelo exportado
	$(PYTHON) src/predict.py --model models/modelo_concreto.joblib

# --- API local ---

api:  ## Levantar la API con FastAPI (modo desarrollo)
	cd despliegue && uvicorn app:app --reload --host 0.0.0.0 --port 8000

# --- Docker ---

docker-prepare:  ## Copiar el modelo al directorio de despliegue
	mkdir -p despliegue/modelo
	cp models/modelo_concreto.joblib despliegue/modelo/

docker: docker-prepare  ## Construir la imagen Docker
	docker build -t concreto-api ./despliegue
	@echo "Imagen construida: concreto-api"

run:  ## Ejecutar el contenedor Docker
	docker run -p 8000:8000 concreto-api

# --- Limpieza ---

clean:  ## Eliminar archivos generados (modelos, cache, etc.)
	rm -rf models/*.joblib models/*.json
	rm -rf __pycache__ src/__pycache__
	rm -rf .ipynb_checkpoints notebooks/.ipynb_checkpoints
	@echo "Archivos generados eliminados."

# --- Ayuda ---

help:  ## Mostrar esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
