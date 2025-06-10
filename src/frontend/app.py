import requests
import streamlit as st
from loguru import logger


def procesar_entrada(entrada: str) -> list[int]:
    """
    Convierte una cadena de texto con enteros separados por comas en una lista de enteros.

    Parámetros:
    ----------
    entrada : str
        Cadena ingresada por el usuario.

    Retorna:
    -------
    list[int]
        Lista de enteros lista para enviar al modelo.
    """
    return [int(x.strip()) for x in entrada.split(",")]


def mostrar_resultado(resultado: dict) -> None:
    """
    Muestra en pantalla la entrada y la salida del modelo con formato legible.

    Parámetros:
    ----------
    resultado : dict
        Diccionario con las claves 'input' y 'output'.
    """
    # Mostrar entrada compacta
    st.subheader("📥 Entrada:")
    st.code(", ".join(str(x) for x in resultado["input"]), language="text")

    # Mostrar salida compacta
    st.subheader("📤 Salida (x2):")
    st.code(", ".join(str(x) for x in resultado["output"]), language="text")


# Configuración de la interfaz
st.set_page_config(page_title="DoubleIt Inference", page_icon="🔁")
st.title("🔁 Inferencia con el modelo DoubleIt")
st.markdown("Este modelo multiplica cada número por 2 usando TorchScript.")

# Entrada del usuario
entrada_usuario = st.text_input(
    "Ingresa una lista de enteros separados por comas", "1, 2, 3, 4"
)

if st.button("🔮 Predicción"):
    logger.info("🔄 Inicio del proceso de inferencia...")

    try:
        # Procesar entrada
        values: list[int] = procesar_entrada(entrada_usuario)
        logger.info(f"✅ Entrada convertida correctamente: {values}")

        # Llamada al backend
        response = requests.post(
            "http://localhost:8000/predict",
            json={"values": values},  # Usa "values" si el backend espera este campo
            timeout=5,
        )
        HTTP_OK = 200
        if response.status_code == HTTP_OK:
            result = response.json()
            logger.info("✅ Respuesta exitosa del servidor.")
            st.success("✅ ¡Predicción realizada con éxito!")
            mostrar_resultado(result)
        else:
            mensaje_error = (
                f"⚠️ Error al llamar a la API. Código de estado: {response.status_code}"
            )
            logger.error(mensaje_error)
            st.error(mensaje_error)

    except ValueError as ve:
        mensaje_error = f"❌ Error al convertir los valores ingresados: {ve}"
        logger.exception(mensaje_error)
        st.error(
            "Por favor, asegúrate de ingresar solo números enteros separados por comas."
        )

    except requests.exceptions.RequestException as re:
        mensaje_error = f"❌ Error en la solicitud al backend: {re}"
        logger.exception(mensaje_error)
        st.error("No se pudo conectar con el backend. Verifica que esté activo.")

    except Exception as e:
        mensaje_error = f"❌ Ocurrió un error inesperado: {e}"
        logger.exception(mensaje_error)
        st.error("Ocurrió un error inesperado. Por favor, intenta nuevamente.")

    finally:
        logger.info("🔚 Proceso de inferencia finalizado.")
