# Guía de Instalación — Taller MLOps UNI

Sigue estos pasos **antes de la primera sesión** para tener tu entorno listo.

---

## Requisitos previos

| Herramienta | Versión mínima | Enlace de descarga |
|---|---|---|
| Python | 3.10+ | https://www.python.org/downloads/ |
| Git | 2.40+ | https://git-scm.com/downloads |
| Docker Desktop | 4.x | https://www.docker.com/products/docker-desktop/ |
| VS Code (recomendado) | — | https://code.visualstudio.com/ |

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/MLOps-Workshop-UNI.git
cd MLOps-Workshop-UNI
```

---

## 2. Crear un entorno virtual

```bash
# Crear el entorno
python -m venv venv

# Activar el entorno
# Linux / macOS:
source venv/bin/activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Windows (CMD):
venv\Scripts\activate.bat
```

---

## 3. Instalar las dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

```bash
# Copiar la plantilla
cp .env.example .env          # Linux/Mac
copy .env.example .env        # Windows CMD
```

Edita el archivo `.env` si necesitas ajustar rutas o credenciales.

---

## 5. Verificar la instalación

```bash
python -c "import sklearn; import pandas; import yaml; print('Todo instalado correctamente')"
```

---

## 6. (Opcional) Instalar DVC

DVC ya está incluido en `requirements.txt`. Para verificar:

```bash
dvc version
```

---

## 7. (Opcional) Verificar Docker

```bash
docker --version
docker run hello-world
```

---

## Problemas comunes

| Problema | Solución |
|---|---|
| `python` no se reconoce | Usa `python3` o verifica que Python está en tu PATH |
| Error de permisos en PowerShell | Ejecuta `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Docker no inicia | Asegúrate de que Docker Desktop está corriendo |
| DVC no se reconoce | Reinstala con `pip install dvc` o verifica tu PATH |

---

¿Listo? ¡Nos vemos en clase!
