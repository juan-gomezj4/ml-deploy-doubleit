from pathlib import Path

import torch
from loguru import logger
from torch import Tensor


class DoubleIt(torch.nn.Module):
    """
    Modelo sencillo que multiplica cada valor de entrada por 2.
    """

    def forward(self, x: Tensor) -> Tensor:
        """
        Método de inferencia del modelo.

        Parámetros:
        ----------
        x : Tensor
            Tensor de entrada.

        Retorna:
        -------
        Tensor
            Tensor con cada valor multiplicado por 2.
        """
        return x * 2


def export_model(output_path: Path) -> None:
    """
    Traza y guarda el modelo en formato TorchScript en la ruta especificada.

    Parámetros:
    ----------
    output_path : Path
        Ruta donde se guardará el modelo trazado.
    """
    try:
        logger.info("⚙️ Inicializando modelo...")
        model: DoubleIt = DoubleIt()
        example_input: Tensor = torch.tensor([1, 2, 3, 4])
        logger.info(f"📥 Ejemplo de entrada: {example_input}")

        traced_model: torch.jit.ScriptModule = torch.jit.trace(model, example_input)
        traced_model.save(str(output_path))

        logger.info(f"✅ Modelo exportado exitosamente a: {output_path}")
    except Exception as err:
        logger.exception("❌ Error durante la exportación del modelo.")
        raise RuntimeError("Error.") from err


if __name__ == "__main__":
    ruta_salida: Path = Path("models/doubleit_model.pt")
    export_model(ruta_salida)
