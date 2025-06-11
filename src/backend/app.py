from fastapi import FastAPI, HTTPException
from loguru import logger

from src.model.load_model import DoubleItModel
from src.model.schema import InputData

# Inicialización de la aplicación FastAPI con metadatos mejorados
app = FastAPI(
    title="Servicio de Inferencia - DoubleIt",
    description="""
    # API de DoubleIt - Multiplicación por 2

    Este proyecto implementa un servicio que utiliza un modelo TorchScript para multiplicar números por 2.
    Incluye una API REST desarrollada con FastAPI y una interfaz de usuario simple construida con Streamlit.

    ## Funcionalidades

    * Procesamiento de listas de números enteros
    * Multiplicación de cada valor por 2 usando un modelo de TorchScript
    * Validación automática de entradas
    * Respuestas estructuradas con los datos originales y resultados

    ## Instrucciones de uso

    La API espera recibir una lista de números enteros y devolverá cada valor multiplicado por 2.
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de ML - Juan Gómez",
        "email": "jgomezja@unal.edu.co",
    },
)
logger.info("🚀 Aplicación FastAPI iniciada.")

# Cargar el modelo al iniciar la aplicación
try:
    model: DoubleItModel = DoubleItModel()
    logger.info("✅ Modelo cargado exitosamente.")
except Exception as err:
    logger.exception("❌ Error al cargar el modelo.")
    raise RuntimeError("Error.") from err


@app.post(
    "/predict",
    response_model=dict[str, list],
    summary="Multiplicar valores por 2",
    description="Recibe una lista de enteros y devuelve cada valor multiplicado por 2 usando el modelo TorchScript",
    response_description="Objeto con la lista de entrada y la lista de salida con valores duplicados",
    status_code=200,
    tags=["Predicción"],
)
def predict(data: InputData) -> dict[str, list]:
    """
    Endpoint que procesa una lista de números enteros y devuelve cada valor multiplicado por 2.

    ## Parámetros

    * **data**: Objeto que contiene una lista de números enteros a multiplicar

    ## Retorna

    Diccionario con:
    * **input**: Lista original de números
    * **output**: Lista con cada número multiplicado por 2

    ## Ejemplos

    Petición:

    ```json
    {
      "values": [1, 2, 3]
    }
    ```

    Respuesta:

    ```json
    {
      "input": [1, 2, 3],
      "output": [2, 4, 6]
    }
    ```

    ## Posibles errores

    * **400**: Entrada inválida - Cuando los datos no cumplen con el formato esperado
    * **500**: Error interno del servidor - Cuando ocurre un error durante el procesamiento
    """
    logger.info("📥 Solicitud de predicción recibida.")
    try:
        resultado = model.predict(data.values)
        logger.info(f"✅ Predicción generada correctamente: {resultado}")
    except ValueError as err:
        logger.exception("❌ Error de validación en los datos de entrada.")
        raise HTTPException(
            status_code=400,
            detail="Entrada inválida. Por favor, proporcione solo números enteros.",
        ) from err
    except Exception as err:
        logger.exception("❌ Error inesperado durante la predicción.")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la predicción.",
        ) from err
    else:
        return {"input": data.values, "output": resultado}
