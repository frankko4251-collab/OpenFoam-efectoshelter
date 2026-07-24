import streamlit as st

# Configuración básica de la página


# Título y descripción
st.title("Simulaciones CFD con OpenFOAM 💨")
st.write("Visualización interactiva de resultados de investigación en dinámica de fluidos.")

# Sección para el primer video

# Código preparado para cuando tengamos el video:
import streamlit as st

st.set_page_config(page_title="Investigación OpenFOAM", layout="wide")

st.info("Explora los diferentes modelos de turbulencia y velocidades.")

# 1. Creamos un diccionario para validar las opciones y mapearlas a los archivos
# (Asegúrate de que estos archivos .mp4 existan en tu carpeta)
modelos_videos = {
    "Modelo k-epsilon - Velocidad Baja": "epsilon 10.mp4",
    "Modelo k-epsilon - Velocidad Alta": "epsilon 18.mp4",
    "Modelo k-omega SST - Velocidad Baja": "omega 10.mp4",
    "Modelo k-omega SST - Velocidad Alta": "omega 18.mp4"
}

# 2. Creamos el menú desplegable en la interfaz
opcion_seleccionada = st.selectbox(
    "Selecciona el modelo y condición a visualizar:",
    list(modelos_videos.keys())
)

# 3. Llamamos al video que corresponde a la selección
archivo_a_mostrar = modelos_videos[opcion_seleccionada]
st.video(archivo_a_mostrar)