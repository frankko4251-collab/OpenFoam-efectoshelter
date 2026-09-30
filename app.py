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

st.header("Geometría del Dominio")
st.info("Interactúa con la maqueta 3D. Gira y haz zoom para explorar.")

# 1. Creamos el interruptor
ver_cotas = st.toggle("Mostrar cotas y medidas", value=True)

# 2. Lógica para ocultar o mostrar
visibilidad_cotas = "block" if ver_cotas else "none"

# 3. Leemos tu archivo 3D (asegúrate de que el nombre sea el correcto, aquí dejé maqueta.glb)
with open("buildings.glb", "rb") as f:
    datos_3d = f.read()
    b64_3d = base64.b64encode(datos_3d).decode("utf-8")

# 4. Inyectamos el visor con tus coordenadas exactas
codigo_html = f'''
<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
<style>
  /* Quitamos el fondo del botón para que no se vea un círculo gris */
  .Hotspot {{
    border: none;
    background: none;
  }}
  
  /* Le damos estilo al cartelito blanco de la cota */
  .HotspotAnnotation {{
    display: {visibilidad_cotas}; /* Aquí se conecta con el interruptor de Streamlit */
    background: white;
    border-radius: 4px;
    padding: 5px 10px;
    font-family: Arial, sans-serif;
    font-size: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.25);
    border: 1px solid #ccc;
  }}
</style>

<model-viewer 
    src="data:model/gltf-binary;base64,{b64_3d}" 
    auto-rotate 
    camera-controls 
    shadow-intensity="1"
    style="width: 100%; height: 500px; background-color: #f4f4f4; border-radius: 10px;">
    
    <!-- Cota 1: Altura 6.6m -->
    <button class="Hotspot" slot="hotspot-2" data-position="-8.284491645009238m 2.856832355316076m 6.9725749521763305m" data-normal="0.20547094633143412m -0.3993009764151941m 0.8934989761871793m">
        <div class="HotspotAnnotation">Altura 6.6 m</div>
    </button>
    
    <!-- Cota 2: Altura 1.2m -->
    <button class="Hotspot" slot="hotspot-4" data-position="5.9664710343985945m 2.9266600608825684m 1.171391566237828m" data-normal="0m -1m 0m">
        <div class="HotspotAnnotation">Altura 1.2 m</div>
    </button>
    
    <!-- Cota 3: Altura 6m -->
    <button class="Hotspot" slot="hotspot-7" data-position="-9.5119758273059m 0.2637165148610574m 6.196090438763218m" data-normal="-0.384493833891953m -0.14521766241229278m 0.911633875096015m">
        <div class="HotspotAnnotation">Altura 6 m</div>
    </button>

</model-viewer>
'''

# 5. Mostramos en pantalla
components.html(codigo_html, height=550)