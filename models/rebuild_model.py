from pathlib import Path

import torch
from loguru import logger
from torch import Tensor


class DoubleIt(torch.nn.Module):
    """
    Reconstrucción del modelo DoubleIt según lógica definida para la prueba técnica.

    Este modelo realiza una operación de inferencia sobre tensores de entrada.
    """

    def forward(self, x: Tensor) -> Tensor:
        """
        Ejecuta la inferencia del modelo reconstruido.

        Parámetros:
        ----------
        x : Tensor
            Tensor de entrada.

        Retorna:
        -------
        Tensor
            Resultado de aplicar la lógica definida en el modelo.
        """
        return x * 2


def export_model(output_path: Path) -> None:
    """
    Reconstruye y guarda el modelo DoubleIt en formato TorchScript.

    Parámetros:
    ----------
    output_path : Path
        Ruta de salida para el archivo .pt generado.
    """
    try:
        logger.info("⚙️ Reconstruyendo modelo DoubleIt...")
        model: DoubleIt = DoubleIt()
        example_input: Tensor = torch.tensor([1, 2, 3, 4])
        logger.info(f"📥 Ejemplo de entrada: {example_input}")

        traced_model: torch.jit.ScriptModule = torch.jit.trace(model, example_input)
        traced_model.save(str(output_path))

        logger.info(f"✅ Modelo reconstruido y exportado a: {output_path}")
    except Exception as err:
        logger.exception("❌ Error durante la reconstrucción del modelo.")
        raise RuntimeError("Error.") from err


if __name__ == "__main__":
    ruta_salida: Path = Path("models/doubleit_model.pt")
    export_model(ruta_salida)
