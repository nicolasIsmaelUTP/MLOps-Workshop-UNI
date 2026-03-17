# Taller MLOps - Empaquetado de Modelos para Producción

**Universidad Nacional de Ingeniería — II Programa de Especialización en IA Generativa y MLOps**

> Taller práctico de 8 horas donde estructuraremos, entrenaremos, empaquetaremos y
> documentaremos un modelo de Machine Learning desde cero, siguiendo buenas prácticas
> de MLOps y reproducibilidad.

---

## Problema

Predecir la **resistencia a la compresión del concreto** (MPa) a partir de 8 variables
de su composición (cemento, escoria, ceniza volante, agua, superplastificante,
agregado grueso, agregado fino y edad de curado).

| Característica | Detalle |
|---|---|
| Dataset | [Concrete Compressive Strength — UCI/Kaggle](https://archive.ics.uci.edu/ml/datasets/concrete+compressive+strength) |
| Registros | 1 030 |
| Features | 8 numéricas |
| Target | `concrete_compressive_strength` (regresión) |
| Modelo base | `RandomForestRegressor` dentro de un Pipeline de Scikit-Learn |

---

## Estructura del Repositorio

```
MLOps-Workshop-UNI/
│
├── .gitignore                 # Archivos y carpetas ignorados por Git
├── .env.example               # Plantilla de variables de entorno (sin secretos)
├── README.md                  # Este archivo (Model Card del proyecto)
├── setup.md                   # Guía de instalación paso a paso
├── requirements.txt           # Dependencias de desarrollo
├── Makefile                   # Comandos rápidos (make train, make predict, etc.)
│
├── configs/
│   └── params.yaml            # Hiperparámetros y rutas centralizadas
│
├── data/
│   ├── raw/                   # Datos originales e inmutables
│   │   └── concrete_data.csv
│   └── processed/             # Datos transformados (generados por código)
│
├── docs/
│   ├── model_card.md          # Documentación técnica del modelo (Model Card)
│   └── presentaciones/        # PDFs de las sesiones teóricas
│
├── models/                    # Modelos serializados (.joblib)
│
├── notebooks/
│   ├── 01_eda.ipynb                              # Exploración de datos
│   ├── 02_pipeline_y_entrenamiento_vacio.ipynb   # Ejercicio para completar en clase
│   └── 02_pipeline_y_entrenamiento_resuelto.ipynb # Solución completa
│
├── src/
│   ├── __init__.py
│   ├── pipeline.py            # Definición del Pipeline (Scaler + Modelo)
│   ├── train.py               # Entrenamiento y exportación del modelo
│   └── predict.py             # Inferencia con el modelo empaquetado
│
└── despliegue/
    ├── app.py                 # API con FastAPI para servir predicciones
    ├── Dockerfile             # Imagen Docker de producción
    └── requirements_deploy.txt # Dependencias mínimas del contenedor
```

---

## Inicio Rápido

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/MLOps-Workshop-UNI.git
cd MLOps-Workshop-UNI

# 2. Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt

# 3. Copiar variables de entorno
cp .env.example .env

# 4. Entrenar el modelo
python src/train.py

# 5. Hacer una predicción de prueba
python src/predict.py

# 6. (Opcional) Levantar la API localmente
cd despliegue
uvicorn app:app --reload
```

O usando el **Makefile**:

```bash
make setup      # Crear entorno e instalar dependencias
make train      # Entrenar y exportar modelo
make predict    # Predicción de prueba
make api        # Levantar API local
make docker     # Construir imagen Docker
```

---

## Sesiones del Taller

| Sesión | Fecha | Temas |
|---|---|---|
| 1 | 25/04/2026 | Fundamentos MLOps, estructura de proyectos, Git/GitHub, DVC |
| 2 | 26/04/2026 | Serialización con joblib, Model Cards, Docker, mini reto final |

---

## Docente

**Nicolás Ismael Alayo Arias** — n_alayo_arias@outlook.com

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.