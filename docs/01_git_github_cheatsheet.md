# Git & GitHub — Cheatsheet MLOps

## Configuración inicial

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

---

## Flujo básico

```bash
git clone https://github.com/<usuario>/<repo>.git   # Clonar un repositorio
cd <repo>

git status                      # Ver estado del workspace
git diff                        # Ver cambios no staged
git add <archivo>               # Área de staging (individual)
git add .                       # Staging de todos los cambios
git commit -m "tipo: mensaje"   # Guardar snapshot en historial
git push origin <rama>          # Subir commits al remoto
git pull origin <rama>          # Bajar y aplicar cambios del remoto
```

---

## Ramas

```bash
git branch                          # Listar ramas locales
git checkout -b <nombre-rama>       # Crear y cambiar a una rama nueva
git checkout <nombre-rama>          # Cambiar a una rama existente
git merge <nombre-rama>             # Fusionar rama dentro de la actual
git branch -d <nombre-rama>         # Eliminar rama local (ya fusionada)
git push origin --delete <rama>     # Eliminar rama en remoto
```

### Convención de nombres (estándar industria)

| Prefijo      | Cuándo usarlo                                         | Ejemplo                             |
|--------------|-------------------------------------------------------|-------------------------------------|
| `feat/`      | Nueva funcionalidad                                   | `feat/agregar-pipeline-limpieza`    |
| `fix/`       | Corrección de error                                   | `fix/error-importacion-pandas`      |
| `exp/`       | Experimento MLOps (puede no llegar a producción)      | `exp/random-forest-200-arboles`     |
| `docs/`      | Solo cambios en documentación                         | `docs/actualizar-model-card`        |
| `chore/`     | Mantenimiento que no afecta el modelo                 | `chore/actualizar-requirements`     |

---

## Experimento típico en MLOps

```bash
# 1. Nunca experimentar en main — crear rama propia
git checkout -b exp/aumentar-n-estimators

# 2. Editar configs/params.yaml (ej. n_estimators: 100 → 200)

# 3. Guardar el experimento
git status
git add configs/params.yaml
git commit -m "exp: aumentar n_estimators a 200"
git push origin exp/aumentar-n-estimators

# 4. Abrir Pull Request en GitHub para revisión antes de fusionar a main
```

---

## Viajes en el tiempo

```bash
git log --oneline                   # Ver historial resumido de commits
git show <hash>                     # Ver detalle de un commit

# Deshacer el último commit (sin perder los cambios, solo deshace el commit)
git reset --soft HEAD~1

# Revertir un commit ya publicado (crea un commit inverso — seguro para main)
git revert <hash-del-commit>
git push origin main
```

> **En ramas protegidas (producción):** nunca uses `reset --hard` ni `push --force` en `main`.  
> Usa siempre `git revert` y abre un PR de emergencia:
> ```bash
> git checkout main && git pull origin main
> git checkout -b fix/revertir-<descripcion>
> git revert <hash>
> git push origin fix/revertir-<descripcion>
> # → Abrir PR en GitHub
> ```

---

## Resolver conflictos de merge

```bash
# 1. Traer la última versión de main
git pull origin main

# 2. Abrir el archivo en conflicto — tendrá marcas como:
# <<<<<<< HEAD
# n_estimators: 200
# =======
# max_depth: 20
# >>>>>>> main

# 3. Editar el archivo dejando la versión correcta (puede incluir ambas líneas)

# 4. Marcar el conflicto como resuelto
git add configs/params.yaml
git commit -m "fix: resolver conflicto de merge en params.yaml"
git push origin <tu-rama>
```

---

## Pull Requests (PR)

| Paso | Acción |
|------|--------|
| 1 | Haz `push` de tu rama al remoto |
| 2 | GitHub muestra botón **"Compare & pull request"** |
| 3 | Describe qué cambiaste y por qué |
| 4 | Revisión del equipo → Aprobación |
| 5 | **Merge** a `main` |
| 6 | Eliminar la rama fuente (GitHub lo ofrece automáticamente) |

**Para revertir un PR ya fusionado:** GitHub → Pestaña *Pull Requests* → *Closed* → Botón **Revert**.

---

## Flujo colaborativo completo

```
fork en GitHub
  ↓
git clone <tu-fork>
  ↓
git checkout -b exp/<descripcion>
  ↓  editar código / params / docs
git add . → git commit → git push origin exp/<descripcion>
  ↓
Pull Request en GitHub → revisión → Merge a main
  ↓
git checkout main && git pull origin main   # sincronizar local
```

---

## Comandos de inspección útiles

```bash
git log --oneline --graph --all    # Árbol visual de ramas y commits
git diff main..mi-rama             # Diferencias entre ramas
git stash                          # Guardar cambios temporalmente sin commitear
git stash pop                      # Restaurar cambios guardados con stash
git blame <archivo>                # Ver quién escribió cada línea
```
