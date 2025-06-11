from fastapi.testclient import TestClient
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.backend.app import app

client = TestClient(app)


def test_predict_route() -> None:
    """
    Prueba el endpoint de predicción '/predict' de la API.

    Esta prueba verifica que el endpoint responda correctamente a una solicitud POST
    con valores de entrada válidos y devuelva la respuesta esperada con los valores
    multiplicados por 2 utilizando el modelo TorchScript.

    Pasos:
    1. Realizar una solicitud POST al endpoint '/predict' con valores [2, 4]
    2. Verificar que el código de estado HTTP sea 200 (OK)
    3. Verificar que la respuesta JSON contenga la entrada original y la salida correcta
       con cada valor multiplicado por 2

    Retorna:
    -------
    None
        La prueba pasa si no se lanzan excepciones y las aserciones son correctas.
    """
    response = client.post("/predict", json={"values": [2, 4]})

    HTTP_200_OK = 200
    assert response.status_code == HTTP_200_OK
    body = response.json()
    assert "input" in body
    assert "output" in body
    assert body["input"] == [2, 4]
    assert body["output"] == [4, 8]


def test_predict_missing_field() -> None:
    """
    Prueba el endpoint '/predict' con un campo faltante en el payload.

    Esta prueba verifica que la API maneje correctamente casos donde el cliente envía
    un JSON con nombres de campo incorrectos, en este caso 'valores' en lugar de 'values'.
    Valida que la API responda con el código de error apropiado según las validaciones
    implementadas con Pydantic.

    Pasos:
    1. Enviar una solicitud POST con el campo mal nombrado ('valores' en vez de 'values')
    2. Verificar que el código de estado sea 422 (Unprocessable Entity)
    3. Verificar que la respuesta contenga detalles sobre el error de validación

    Retorna:
    -------
    None
        La prueba pasa si las aserciones sobre el código de estado y la estructura
        de la respuesta de error son correctas.
    """
    response = client.post("/predict", json={"valores": [1, 2]})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    body = response.json()
    assert "detail" in body
    assert isinstance(body["detail"], list)


def test_predict_invalid_type() -> None:
    """
    Prueba el endpoint '/predict' con un tipo de dato inválido para 'values'.

    Esta prueba verifica que la API valide correctamente el tipo de datos enviado
    en el campo 'values', rechazando valores que no sean listas como se espera
    según la definición del modelo InputData con Pydantic.

    Pasos:
    1. Enviar una solicitud POST con 'values' como string en lugar de lista
    2. Verificar que el código de estado sea 422 (Unprocessable Entity)
    3. Verificar que la respuesta contenga detalles específicos sobre el error de tipo
    4. Comprobar que el error indique correctamente la ubicación y tipo del error

    Retorna:
    -------
    None
        La prueba pasa si las aserciones sobre el código de estado y los detalles
        específicos del error de validación son correctos.
    """
    response = client.post("/predict", json={"values": "no_es_lista"})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    body = response.json()
    assert "detail" in body
    assert body["detail"][0]["loc"] == ["body", "values"]
    assert body["detail"][0]["type"] == "list_type"
