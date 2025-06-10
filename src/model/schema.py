from loguru import logger
from pydantic import BaseModel, Field, ValidationError


class InputData(BaseModel):
    """
    Modelo de entrada para la API.

    Contiene una lista de números enteros que serán procesados por el modelo.
    """

    values: list[int] = Field(
        ..., min_length=1, description="Lista de números enteros (al menos uno)"
    )

    def __init__(self, **data: object) -> None:
        """
        Inicializa y valida los datos de entrada.
        Registra logs informativos y maneja errores de validación.
        """
        try:
            super().__init__(**data)
            logger.info(f"✅ Datos de entrada validados correctamente: {self.values}")

        except ValidationError:
            logger.exception("❌ Error de validación en los datos de entrada.")
            raise
