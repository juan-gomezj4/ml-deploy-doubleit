from src.model.load_model import DoubleItModel


def test_model_prediction() -> None:
    """
    Prueba la funcionalidad básica de predicción del modelo DoubleItModel.

    Esta prueba verifica que el modelo cargue correctamente y que las predicciones
    funcionen como se espera, multiplicando cada valor de entrada por 2.

    Pasos:
    1. Inicializar una instancia del modelo DoubleItModel
    2. Realizar una predicción con una lista de enteros [1, 2, 3]
    3. Verificar que el resultado sea [2, 4, 6]

    Retorna:
    -------
    None
        La prueba pasa si no se lanzan excepciones y las aserciones son correctas.
    """
    model = DoubleItModel()
    result = model.predict([1, 2, 3])
    assert result == [2, 4, 6]
