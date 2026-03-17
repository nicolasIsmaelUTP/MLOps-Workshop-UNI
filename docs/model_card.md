# Model Card — Predicción de Resistencia del Concreto

## Información General

| Campo | Detalle |
|---|---|
| **Nombre del modelo** | modelo_concreto |
| **Versión** | 1.0 |
| **Tipo** | Regresión |
| **Framework** | Scikit-Learn 1.6.1 |
| **Arquitectura** | Pipeline(StandardScaler + RandomForestRegressor) |
| **Fecha de entrenamiento** | YYYY-MM-DD |
| **Autor(es)** | Participantes del Taller MLOps — UNI |

---

## Descripción

Modelo de Machine Learning que predice la **resistencia a la compresión del concreto**
(en MPa) a partir de la composición de la mezcla y la edad de curado.

El modelo está empaquetado como un Pipeline de Scikit-Learn que incluye el
preprocesamiento (escalado estándar) y el regresor, eliminando el riesgo de
**Train-Serve Skew**.

---

## Datos de Entrenamiento

- **Fuente**: UCI Machine Learning Repository — Concrete Compressive Strength
- **Registros totales**: 1 030
- **Split**: 80% entrenamiento / 20% prueba (random_state=42)

---

## Variables de Entrada (Features)

| # | Feature | Unidad | Descripción |
|---|---|---|---|
| 1 | `cement` | kg/m³ | Cantidad de cemento |
| 2 | `blast_furnace_slag` | kg/m³ | Escoria de alto horno |
| 3 | `fly_ash` | kg/m³ | Ceniza volante |
| 4 | `water` | kg/m³ | Cantidad de agua |
| 5 | `superplasticizer` | kg/m³ | Superplastificante |
| 6 | `coarse_aggregate` | kg/m³ | Agregado grueso |
| 7 | `fine_aggregate` | kg/m³ | Agregado fino |
| 8 | `age` | días | Edad de curado |

---

## Variable de Salida (Target)

| Variable | Unidad | Rango |
|---|---|---|
| `concrete_compressive_strength` | MPa | ~2.3 — ~82.6 |

---

## Métricas de Evaluación

> Completar después del entrenamiento:

| Métrica | Valor |
|---|---|
| MAE (Mean Absolute Error) | 3.7382 |
| RMSE (Root Mean Squared Error) | 5.4638 |
| R² (Coeficiente de determinación) | 0.8841 |

---

## Uso

### Inferencia con Python

```python
import joblib
import numpy as np

pipeline = joblib.load("models/modelo_concreto.joblib")

# Ejemplo: una muestra con 8 features
muestra = np.array([[540.0, 0.0, 0.0, 162.0, 2.5, 1040.0, 676.0, 28]])
prediccion = pipeline.predict(muestra)
print(f"Resistencia predicha: {prediccion[0]:.2f} MPa")
```

### Inferencia con la API (curl)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cement": 540.0,
    "blast_furnace_slag": 0.0,
    "fly_ash": 0.0,
    "water": 162.0,
    "superplasticizer": 2.5,
    "coarse_aggregate": 1040.0,
    "fine_aggregate": 676.0,
    "age": 28
  }'
```

---

## Limitaciones y Supuestos

- El modelo fue entrenado exclusivamente con datos del dataset UCI Concrete.
- No generaliza a tipos de concreto con composiciones fuera del rango de entrenamiento.
- No incluye variables ambientales (temperatura, humedad) que afectan el fraguado.
- Uso exclusivamente educativo — no validado para decisiones de ingeniería civil real.

---

## Consideraciones Éticas

- Este modelo es un ejercicio académico del Taller MLOps de la UNI.
- No debe usarse para tomar decisiones estructurales en proyectos de construcción.
