from fastapi import FastAPI, HTTPException
from loguru import logger

from src.model.load_model import DoubleItModel
from src.model.schema import InputData

# Inicialización de la aplicación FastAPI
app = FastAPI(title="Servicio de Inferencia - DoubleIt")
logger.info("🚀 Aplicación FastAPI iniciada.")

# Cargar el modelo al iniciar la aplicación
try:
    model: DoubleItModel = DoubleItModel()
    logger.info("✅ Modelo cargado exitosamente.")
except Exception as err:
    logger.exception("❌ Error al cargar el modelo.")
    raise RuntimeError("Error.") from err


@app.post("/predict", response_model=dict[str, list])
def predict(data: InputData) -> dict[str, list]:
    """
    Endpoint que recibe una lista de números enteros y devuelve la predicción generada por el modelo.

    Parámetros:
    ----------
    data : InputData
        Objeto con la lista de enteros a procesar.

    Retorna:
    -------
    dict[str, list]
        Diccionario con la entrada original y el resultado de la predicción.
    """
    logger.info("📥 Solicitud de predicción recibida.")
    try:
        resultado = model.predict(data.values)
        logger.info(f"✅ Predicción generada correctamente: {resultado}")
    except ValueError as err:
        logger.exception("❌ Error de validación en los datos de entrada.")
        raise HTTPException(status_code=400, detail="Entrada inválida") from err
    else:
        return {"input": data.values, "output": resultado}
