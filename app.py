import streamlit as st

# Configuración básica
st.set_page_config(page_title="Investigación OpenFOAM", layout="wide")

# --- NUEVA SECCIÓN DE LOGOS ---
# Creamos tres columnas: las de los extremos (tamaño 1) para los logos, 
# y una muy ancha en el centro (tamaño 4) para separarlos.
col_logo1, col_espacio, col_logo2 = st.columns([1, 4, 1])

with col_logo1:
    # Asegúrate de poner el nombre exacto de tu imagen de la UTN
    st.image("logo UTNFRM.png", use_container_width=True)

with col_logo2:
    # Asegúrate de poner el nombre exacto de tu imagen del IEMI
    st.image("Logo Iemi.png", use_container_width=True)
# ------------------------------

st.title("Simulaciones CFD con OpenFOAM ")
st.write("Visualización interactiva de resultados de investigación en dinámica de fluidos.")

# 1. Creamos la casilla de verificación
modo_comparacion = st.checkbox("Activar modo de comparación simultánea")

st.divider() # Agrega una línea horizontal para separar secciones visualmente

# 2. Lógica para decidir qué mostrar
if modo_comparacion:
    # Si la casilla ESTÁ marcada, mostramos las dos columnas
    st.header("Comparación de Modelos de Turbulencia")
    st.info("Comparativa directa entre los modelos para altas velocidades.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Modelo k-epsilon")
        st.video("epsilon 18_2.mp4") # Reemplaza con tus nombres reales
        
    with col2:
        st.subheader("Modelo k-omega")
        st.video("omega 18_2.mp4") # Reemplaza con tus nombres reales

else:
    # Si la casilla NO está marcada, mostramos la vista individual
    st.header("Visualización Individual")
    
    # Diccionario con las opciones
    modelos_videos = {
        "Modelo k-epsilon - Velocidad Baja": "epsilon 10_2.mp4",
        "Modelo k-epsilon - Velocidad Alta": "epsilon 18_2.mp4",
        "Modelo k-omega - Velocidad Baja": "omega 10_2.mp4",
        "Modelo k-omega - Velocidad Alta": "omega 18_2.mp4"
    }
    
    opcion_seleccionada = st.selectbox(
        "Selecciona el modelo y condición a visualizar:",
        list(modelos_videos.keys())
    )
    
    archivo_a_mostrar = modelos_videos[opcion_seleccionada]
    st.video(archivo_a_mostrar)