FROM python:3.11-slim

WORKDIR /app

# Instalar UV
RUN pip install uv

# Copiar los archivos de dependencias y sincroniza el entorno
COPY pyproject.toml uv.lock ./
RUN uv sync --group front

# Copiar el código fuente y modelo
COPY src ./src
COPY models ./models

# Exponer el puerto por defecto de Streamlit
EXPOSE 8080

# Ejecutar Streamlit usando el puerto de entorno
CMD ["uv", "run", "streamlit", "run", "src/frontend/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
