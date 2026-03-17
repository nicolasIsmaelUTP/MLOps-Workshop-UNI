# ============================================================
# Dockerfile — API de Predicción de Resistencia del Concreto
# ============================================================
# Construir:  docker build -t concreto-api ./despliegue
# Ejecutar:   docker run -p 8000:8000 concreto-api
# Probar:     curl http://localhost:8000/
# ============================================================

FROM python:3.10-slim

# Metadata
LABEL maintainer="Taller MLOps UNI"
LABEL description="API de predicción de resistencia del concreto"

# Evitar prompts interactivos y buffering de Python
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar SOLO las dependencias de producción
COPY requirements_deploy.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements_deploy.txt

# Copiar el código de la API y el modelo serializado
COPY app.py .
COPY modelo/modelo_concreto.joblib modelo/modelo_concreto.joblib

# Exponer el puerto de la API
EXPOSE 8000

# Comando para iniciar la API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
