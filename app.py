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
    # Si la casilla ESTÁ marcada, mostramos el video unificado
    st.header("Comparación de Modelos de Turbulencia")
    st.info("Comparativa directa: Modelo k-epsilon (izq.) vs Modelo k-omega (der.)")
     
    st.video("Comparación modelo k-ep_k-om.mp4") 

else:
    # Si la casilla NO está marcada, mostramos la vista individual
    st.header("Visualización Individual")
    
        
    # Diccionario con las opciones
    modelos_videos = {
        "Modelo k-epsilon - Velocidad Baja": "epsilon 10_2.mp4",
        "Modelo k-epsilon - Velocidad Alta": "epsilon 18_2.mp4",
        "Modelo k-omega - Velocidad Baja": "omega 10_2.mp4",
        "Modelo k-omega - Velocidad Alta": "omega18_2.mp4"
    }
    
    opcion_seleccionada = st.selectbox(
        "Selecciona el modelo y condición a visualizar:",
        list(modelos_videos.keys())
    )
    
    archivo_a_mostrar = modelos_videos[opcion_seleccionada]
    st.video(archivo_a_mostrar)

import streamlit.components.v1 as components
import base64

st.header("Geometría del Dominio 🌳")
st.info("Interactúa con la maqueta 3D de los setos y viñedos. Gira y haz zoom para explorar.")

# 1. Leemos el archivo 3D y lo codificamos para la web
with open("buildings.glb", "rb") as f:
    datos_3d = f.read()
    b64_3d = base64.b64encode(datos_3d).decode("utf-8")

# 2. Creamos el visor interactivo (model-viewer)
codigo_html = f'''
<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
<model-viewer 
    src="data:model/gltf-binary;base64,{b64_3d}" 
    auto-rotate 
    camera-controls 
    shadow-intensity="1"
    style="width: 100%; height: 500px; background-color: #f4f4f4; border-radius: 10px;">
</model-viewer>
'''

# 3. Lo mostramos en la página de Streamlit
components.html(codigo_html, height=520)