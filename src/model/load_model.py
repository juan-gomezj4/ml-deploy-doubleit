from pathlib import Path
from typing import cast

import torch
from loguru import logger
from torch import Tensor

# Ruta del modelo TorchScript
MODEL_PATH: Path = Path("models/doubleit_model.pt")


class DoubleItModel:
    """
    Clase encargada de cargar el modelo TorchScript y ejecutar inferencias sobre entradas numéricas.
    """

    def __init__(self) -> None:
        """
        Inicializa la clase cargando el modelo desde el archivo especificado.
        Lanza RuntimeError si el modelo no puede ser cargado correctamente.
        """
        try:
            self.model: torch.jit.ScriptModule = torch.jit.load(str(MODEL_PATH))
            logger.info("✅ Modelo DoubleIt cargado correctamente desde el archivo.")
        except Exception as err:
            logger.exception("❌ Error al cargar el modelo desde la ruta especificada.")
            raise RuntimeError("Error.") from err

    def predict(self, values: list[int]) -> list[int]:
        """
        Realiza la inferencia sobre una lista de enteros utilizando el modelo cargado.

        Parámetros:
        ----------
        values : list[int]
            Lista de números enteros que se desean duplicar.

        Retorna:
        -------
        list[int]
            Lista de enteros resultantes luego de aplicar el modelo.

        Lanza:
        -----
        RuntimeError: si ocurre un error durante la inferencia.
        """
        try:
            tensor_input: Tensor = torch.tensor(values)
            logger.debug(f"📊 Entrada convertida a tensor: {tensor_input}")

            with torch.no_grad():
                output: Tensor = self.model(tensor_input)
                logger.info(f"✅ Predicción completada con éxito: {output.tolist()}")

            return cast(list[int], output.tolist())
        except Exception as err:
            logger.exception("❌ Error durante la inferencia del modelo.")
            raise RuntimeError("Error.") from err
