# TorchScript Model Deployment: DoubleIt API - Streamlit App

# 🔧 Descripción del Proyecto

Este repositorio contiene una solución completa para desplegar un modelo TorchScript llamado **DoubleIt**, cuyo objetivo es multiplicar una lista de números por 2

La finalidad principal del reto es **poner en producción este modelo** utilizando buenas prácticas de ingeniería, cubriendo los siguientes aspectos clave:

- Containerización del modelo y su API
- Pruebas unitarias con cobertura
- Automatización del despliegue (`dev`) mediante CI/CD con GitHub Actions
- Infraestructura como código (IaC) con Terraform
- Separación de entornos (`dev` y `prod`) para facilitar pruebas y despliegues controlados

Se asume que la inferencia se realiza vía una llamada síncrona desde un backend (FastAPI) a un modelo TorchScript, y se expone una interfaz simple mediante Streamlit para facilitar la interacción

El modelo ya entrenado se encuentra serializado en formato TorchScript y listo para su consumo

# 📁 Estructura del Repositorio

La siguiente estructura organiza el proyecto en módulos funcionales y componentes reutilizables:

```
├── codecov.yml                                     # Configuración de cobertura para Codecov
│
├── docker/
│ ├── backend/Dockerfile                            # Imagen Docker del backend (FastAPI)
│ └── frontend/Dockerfile                           # Imagen Docker del frontend (Streamlit)
│
├── docker-compose.yml                              # Orquestación local de backend y frontend
│
├── iac/                                            # Infraestructura como código (Terraform)
│ ├── main.tf
│ ├── outputs.tf
│ ├── terraform.tfvars
│ └── variables.tf
│
├── infra_setup.sh                                  # Script para automatizar Terraform + GitHub Secret
│
├── Makefile                                        # Comandos utilitarios para test, lint, terraform
│
├── models/                                         # Carpeta con modelo TorchScript
│ ├── doubleit_model/                               # Representación detallada del modelo
│ ├── doubleit_model.pt                             # Modelo TorchScript serializado
│ ├── inference_example.py                          # Script para pruebas manuales del modelo
│ └── rebuild_model.py                              # Reconstrucción del modelo desde PyTorch
│
├── pyproject.toml                                  # Metadata del proyecto, dependencias y configuración de herramientas
│
├── README.md                                       # Documentación del proyecto
│
├── src/                                            # Código fuente
│ ├── backend/app.py                                # API REST para predicción
│ ├── frontend/app.py                               # Interfaz Streamlit
│ ├── model/
│ │ ├── load_model.py                               # Lógica de carga y uso del modelo
│ │ └── schema.py                                   # Validación con Pydantic
│ └── tmp_mock.py                                   # Módulo de prueba para pre-commit
│
├── tests/                                          # Pruebas unitarias
│ ├── test_backend.py
│ ├── test_mock.py
│ └── test_model.py
│
└── uv.lock                                        # Archivo de dependencias generado por UV
```

# 📦 Model Deployment: Componentes Principales

Este proyecto implementa un flujo completo de MLOps para un modelo TorchScript (`doubleit_model.pt`), usando FastAPI como backend de inferencia y Streamlit como interfaz de usuario.

### 🔁 Backend (FastAPI)
- **Ubicación:** `src/backend/app.py`
- **Objetivo:** Proveer un endpoint REST (`/predict`) para inferencia sobre listas de enteros
- **Carga del modelo:** `load_model.py` usa `torch.jit.load` para deserializar el modelo TorchScript
- **Validación:** `schema.py` valida entradas usando `pydantic`

### 🖥️ Frontend (Streamlit)
- **Ubicación:** `src/frontend/app.py`
- **Objetivo:** Recibir entrada del usuario, llamar al backend y mostrar la predicción
- **Comunicación:** HTTP POST al endpoint `/predict` del backend

### 📦 Empaquetamiento (Docker)
- **Dockerfiles:** Separados para backend y frontend
- **docker-compose:** Orquesta ambos servicios localmente, expuestos en puertos 8000 y 8501 respectivamente
- **Build multiplataforma:** `--platform linux/amd64` para compatibilidad con Cloud Run

### 🌐 Despliegue (Cloud Run)
- **Backend y frontend:** se despliegan como servicios independientes (`doubleit-backend-dev`, `doubleit-frontend-dev`)
- **Autenticación:** pública (`--allow-unauthenticated`) para facilitar acceso
- **Deploy automatizado:** vía GitHub Actions

### 📦 Modelo TorchScript
- **Archivo principal:** `doubleit_model.pt`
- **Reconstrucción:**  en base a la estructura compartida, empleando el script `rebuild_model.py`
- **Inferencia:** Entrada → tensor → salida multiplicada por 2

# 🐳 Containerización

La solución se empaqueta mediante contenedores Docker separados para el backend y el frontend. Esto garantiza portabilidad, aislamiento y compatibilidad con entornos de ejecución -como Cloud Run-

### 📁 Archivos relevantes

- `docker/backend/Dockerfile`: construye la imagen para el servicio FastAPI
- `docker/frontend/Dockerfile`: construye la imagen para el servicio Streamlit
- `docker-compose.yml`: permite ejecutar ambos servicios localmente con un solo comando

### 💡 Detalles técnicos

- **Base image:** `python:3.11-slim` (ligera y optimizada)
- **Gestor de dependencias:** `uv` con `pyproject.toml` y `uv.lock`
- **Entrypoints:**
  - Backend: `uvicorn src.backend.app:app`
  - Frontend: `streamlit run src/frontend/app.py`
- **Compatibilidad Cloud Run:** Se utiliza arquitectura `linux/amd64` en CI/CD para asegurar compatibilidad con ambientes x86_64

# 🧪 Pruebas Unitarias y Cobertura

El proyecto incluye pruebas unitarias para validar el comportamiento del modelo y el backend

### 📁 Estructura de pruebas
```
tests/
├── test_backend.py                                 # Pruebas del endpoint FastAPI
├── test_model.py                                   # Pruebas del modelo TorchScript
├── test_mock.py                                    # Prueba para validar CI y pre-commit
```

### ✅ Cobertura

- Se utiliza `pytest` junto con `pytest-cov` para medir la cobertura de código
- Los comandos están integrados en el `Makefile`:
  - `make test`: ejecuta pruebas con cobertura
  - `make test_verbose`: modo detallado
  - `make test_coverage`: genera reporte XML para Codecov

### 📊 Codecov

El archivo codecov.yml define umbrales mínimos y tolerancias para garantizar calidad continua

# 🌐 Estrategia de Entornos: Dev vs Prod

Aunque el requirimiento no exigía una implementación real en la nube y aceptaba una propuesta estructural, esta solución fue llevada a producción sobre Google Cloud Platform como una demostración práctica de dominio técnico y alineación con estándares reales de despliegue en la industria

Se plantea una separación clara entre los entornos `dev` y `prod`, cada uno con responsabilidades bien definidas:

### 🔁 Entorno `dev` — Automatización vía CI/CD

- **Objetivo:** pruebas rápidas, validación continua y despliegue inmediato tras cada cambio en el repositorio
- **Implementación:** GitHub Actions ejecuta el flujo completo de CI/CD, que incluye:
  - Instalación del entorno
  - Linter, formateo y validaciones de estilo (`pre-commit`)
  - Pruebas unitarias y cobertura
  - Construcción y despliegue de imágenes Docker a Cloud Run
- **Servicios desplegados:** `doubleit-backend-dev`, `doubleit-frontend-dev`
- **Acceso:** público (`--allow-unauthenticated`)
- **Conexión:** la URL del backend se pasa como variable de entorno al frontend en tiempo de despliegue

### 🔒 Entorno `prod` — Provisionamiento con Terraform

- **Objetivo:** entorno estable y controlado, con posibilidad de configuraciones específicas como autenticación, dominios personalizados o escalado avanzado
- **Implementación:** Terraform permite crear toda la infraestructura necesaria, incluyendo cuentas de servicio, repositorios en Artifact Registry y servicios en Cloud Run
- **Estado actual:** el entorno `prod` no fue desplegado, pero su definición está completamente lista para ejecutarse siguiendo el mismo flujo

### 🧱 Relación entre ambos entornos

- Terraform define los **recursos base compartidos**, como el Artifact Registry y la cuenta de servicio que usa GitHub Actions
- GitHub Actions usa estos recursos para desplegar el entorno `dev`
- En un contexto real, Terraform permitiría extender esta lógica para crear el entorno `prod`, asegurando separación, versionado y buenas prácticas de infraestructura

Esta arquitectura híbrida permite un desarrollo ágil en `dev` y una base sólida para un entorno `prod` preparado para escalar

# ⚙️ CI/CD con GitHub Actions (Entorno Dev)

El entorno de desarrollo (`dev`) se despliega automáticamente mediante un pipeline de GitHub Actions que ejecuta los siguientes pasos:

### 🔄 Flujo CI/CD

1. **CI (Integración Continua):**
   - **Pre-commit hooks:** validación de estilo con `ruff` y `black`
   - **Pruebas unitarias:** ejecución con `pytest` y generación de reporte de cobertura con `coverage`
   - **Subida de cobertura:** integración con Codecov

2. **CD (Despliegue Continuo):**
   - **Autenticación con GCP:** usando una cuenta de servicio configurada como secreto (`GCP_CREDENTIALS`)
   - **Build de imágenes Docker:** para backend y frontend, incluyendo arquitectura `linux/amd64` para compatibilidad con Cloud Run
   - **Push a Artifact Registry.**
   - **Despliegue en Cloud Run:** con `--memory=1Gi` y `--allow-unauthenticated`.

### 🚀 Jobs del Workflow

```yaml
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint-and-format:
    ...

  test:
    ...

  build-and-deploy:
    ...
```

### 🧩 Variables y secretos utilizados

- GCP_CREDENTIALS: clave JSON de la cuenta de servicio
- GCP_PROJECT_ID: ID del proyecto
- GCP_REGION: región donde se despliega (us-central1)
- BACKED_URL: pasado como variable al frontend para consumo del API

Este flujo garantiza un entorno funcional cada vez que se hace push a main, permitiendo validar en caliente los cambios de backend y frontend sobre GCP

# 🛠️ Infraestructura como Código (IaC)

La infraestructura base fue definida con Terraform, siguiendo el enfoque de separar los recursos compartidos del despliegue por entorno. El objetivo es centralizar la creación de componentes reutilizables (como cuentas de servicio y repositorios) y habilitar entornos con configuraciones distintas según sea `dev` o `prod`

### 📦 Recursos creados por Terraform

- **`Service Account`**: `github-deployer` con los siguientes roles:
  - `roles/run.admin`
  - `roles/artifactregistry.admin`
  - `roles/cloudbuild.builds.editor`
  - `roles/iam.serviceAccountUser`

- **`Artifact Registry`**:
  - Repositorio Docker: `ml-deploy-repo` en `us-central1`

### 🚀 Flujo de uso local

Se automatiza con `Makefile` y un script `infra_setup.sh`:

```bash
bash infra_setup.sh
```

Este script ejecuta:

1. terraform init y terraform apply

2. Crea la clave JSON de la cuenta de servicio

3. Sube la clave como secreto a GitHub (GCP_CREDENTIALS)

4. Elimina la clave local por seguridad

### 🧭 Extensión hacia prod

La misma lógica permite escalar la infraestructura:

- Crear servicios separados (doubleit-backend-prod, doubleit-frontend-prod)
- Ajustar memoria, seguridad y dominios
- Activar autenticación y políticas más estrictas

Aunque en esta prueba solo se desplegó dev vía CI/CD, la arquitectura está preparada para soportar múltiples entornos gestionados por Terraform

# 🚀 Cómo Ejecutar Localmente

### Pasos:

1. Clonar el repositorio
2. Instalar Docker y Docker Compose
3. Ejecutar `docker-compose up --build` para levantar backend y frontend
4. Acceder al backend en `http://localhost:8000/docs`
5. Acceder al frontend en `http://localhost:8501`
6. Instalar [uv]
7. Ejecutar `uv sync --all-groups` para instalar dependencias
8. Ejecutar pruebas con `make test`


# ☁️ Cómo Desplegar en GCP

### Pasos:

1. Crear un proyecto en GCP (ej. `ml-deploy-doubleit`)
2. Activar las APIs necesarias:
   - Cloud Run
   - Artifact Registry
   - IAM
3. Clonar este repositorio y posicionarse en la raíz del proyecto
4. Crear el archivo `.env` desde `.env.example` con:
   - `PROJECT_ID`
   - `SA_NAME`
   - `REGION`
5. Ejecutar `bash infra_setup.sh` para:
   - Crear la cuenta de servicio `github-deployer`
   - Crear el repositorio `ml-deploy-repo` en Artifact Registry
   - Asignar permisos mínimos a la cuenta
   - Generar la clave JSON y subirla como secreto en GitHub
6. Verificar que en GitHub existan los secretos:
   - `GCP_CREDENTIALS`
   - `GCP_PROJECT_ID`
   - `GCP_REGION`
7. Hacer `git push` a `main` y dejar que GitHub Actions despliegue automáticamente en Cloud Run
8. Consultar las URLs generadas en la consola de Cloud Run (backend y frontend)


# 📈 Consideraciones de Monitoreo, Versionamiento y Seguridad

Se proponen las siguientes prácticas adicionales para entornos productivos:

### 🩺 Monitoreo
- **Cloud Logging & Monitoring**: Cloud Run exporta logs automáticamente a Google Cloud Logging. Se pueden crear alertas en Cloud Monitoring para:
  - Errores HTTP 5xx
  - Fallos en despliegues
  - Superación de umbrales de memoria/CPU

### 🧬 Versionamiento de Modelos
- **Artifact Registry** gestiona versiones de imágenes (`doubleit-backend:1.0.0`, `doubleit-backend:latest`, etc.)
- **Modelo TorchScript** puede versionarse por nombre de archivo y almacenarse en Cloud Storage o Artifact Registry
- Uso de etiquetas y ramas en Git para separar releases (`main`, `prod`, `v1.0`)

### 🔐 Seguridad
- **Mínimos privilegios**: la cuenta de servicio de CI/CD tiene solo los roles estrictamente necesarios
- **Secretos gestionados en GitHub**: la clave JSON no se sube al repo, se inyecta como secreto
- **Accesos**:
  - El entorno `dev` permite acceso público (`--allow-unauthenticated`)
  - El entorno `prod` puede configurarse con autenticación o IP filtering

