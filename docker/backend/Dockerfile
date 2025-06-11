FROM python:3.11-slim

WORKDIR /app

# Instalar UV
RUN pip install uv

# Copiar archivos de dependencias y sincronizar entorno
COPY pyproject.toml uv.lock ./
RUN uv sync --group back

# Copiar código fuente y modelos
COPY src ./src
COPY models ./models

# Exponer el puerto de FastAPI
EXPOSE 8000

# Ejecutar FastAPI en modo producción
CMD ["uv", "run", "uvicorn", "src.backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
