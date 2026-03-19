# DVC — Cheatsheet de Comandos

## Instalación e inicialización

```bash
pip install dvc            # Instalar DVC
dvc version                # Verificar instalación
dvc init                   # Inicializar DVC en un repo Git existente
```

---

## Versionamiento de datos

```bash
dvc add data/raw/archivo.csv          # Rastrear un archivo con DVC
git add data/raw/archivo.csv.dvc data/raw/.gitignore
git commit -m "data: versionar dataset con DVC"
```

> DVC calcula un hash MD5, mueve el archivo a `.dvc/cache/` y crea un puntero `.dvc` que Git sí puede rastrear.

---

## Almacenamiento remoto

```bash
# Crear y configurar un remoto (local, S3, GCS, Azure, etc.)
dvc remote add -d mi_remoto /ruta/al/storage
dvc remote add -d s3_remoto s3://mi-bucket/dvc

git add .dvc/config
git commit -m "config: añadir remoto de DVC"
```

---

## Push / Pull de datos

```bash
dvc push          # Subir datos al remoto (análogo a git push)
dvc pull          # Descargar datos del remoto (análogo a git pull)
dvc fetch         # Descargar al caché local sin copiar al workspace
```

---

## Sincronizar datos al cambiar de rama / commit

```bash
git checkout main       # 1. Cambia rama en Git (solo actualiza el puntero .dvc)
dvc checkout            # 2. Restaura el CSV real que corresponde a ese puntero
```

---

## Actualizar un dataset

```bash
# 1. Edita / reemplaza tu archivo CSV
dvc add data/raw/archivo.csv          # Re-registra los cambios
git add data/raw/archivo.csv.dvc
git commit -m "data: actualizar dataset con nuevas muestras"
dvc push                              # Empuja la nueva versión al remoto
```

---

## Pipelines (dvc.yaml)

```bash
# Definir una etapa del pipeline
dvc stage add -n etapa \
              -d src/script.py -d data/raw/entrada.csv \
              -o data/processed/salida.csv \
              python src/script.py

dvc repro          # Ejecutar / reproducir el pipeline completo
dvc dag            # Visualizar el grafo de dependencias del pipeline
dvc status         # Ver qué etapas están desactualizadas
```

---

## Experimentos

```bash
dvc exp run                        # Ejecutar un experimento
dvc exp show                       # Tabla comparativa de experimentos
dvc exp diff                       # Diferencias entre experimentos
dvc exp apply <exp-name>           # Aplicar un experimento al workspace
```

---

## Mantenimiento de caché

```bash
dvc gc -w          # Elimina de la caché local todo lo que NO use el workspace actual
                   # (el remoto no se ve afectado)
```

---

## Estado e inspección

```bash
dvc status                    # Muestra archivos desactualizados respecto al caché
dvc list . --dvc-only         # Lista los archivos rastreados por DVC
dvc params diff               # Diferencias en parámetros entre commits
dvc metrics show              # Muestra métricas del pipeline
dvc metrics diff              # Compara métricas entre commits
```

---

## Flujo de trabajo típico

```
git clone <repo>          # Clonar el proyecto (solo código + punteros .dvc)
dvc pull                  # Descargar los datos reales desde el remoto
# ... trabajar, editar datos o código ...
dvc repro                 # Reproducir el pipeline
dvc push                  # Subir datos/modelos nuevos al remoto
git add .  ;  git push    # Registrar cambios de código y punteros en Git
```
