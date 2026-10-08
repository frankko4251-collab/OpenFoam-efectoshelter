import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
import plotly.graph_objects as go

# Configuración básica
st.set_page_config(page_title="Investigación OpenFOAM", layout="wide")

# --- FUNCIONES AUXILIARES PARA GRÁFICOS ---
@st.cache_data
def cargar_datos(archivo):
    # La caché evita que Streamlit lea el archivo desde cero cada vez que movemos el botón
    return pd.read_csv(archivo)

def graficar_estela(df, velocidad, titulo):
    # Filtramos por velocidad
    zona_estela = df[df['U_mag'] <= velocidad]
    
    if not zona_estela.empty:
        # Agrupamos por cada distancia X y buscamos la altura máxima
        curva_estela = zona_estela.groupby('X_rel')['z'].max().reset_index()
        
        # 1. Dibujamos la gráfica base
        figura = px.line(
            curva_estela, 
            x='X_rel', 
            y='z', 
            title=titulo,
            labels={'X_rel': 'Distancia aguas abajo (m)', 'z': 'Altura (m)'}
        )
        
        # 2. Replicamos el estilo "escalonado" y el sombreado
        figura.update_traces(
            fill='tozeroy', 
            line_color='#1f77b4', 
            fillcolor='rgba(31, 119, 180, 0.15)',
            line_shape='vh', # Esto genera el efecto escalonado de tu gráfica original
            name=f'Estela (U = {velocidad} m/s)',
            showlegend=True
        )
        
        # 3. Mover el "cero" a la derecha configurando el rango del eje X
        max_x = curva_estela['X_rel'].max()
        # El eje empieza en -5 y termina un poco después del último punto
        figura.update_xaxes(range=[-5, max_x + 5]) 
        
        # 4. Agregar la Cortina Forestal
        figura.add_trace(go.Scatter(
            x=[0, 0], 
            y=[0, 6.6], 
            mode="lines", 
            line=dict(color="grey", width=5),
            name="Cortina Forestal"
        ))
        
        # 5. Agregar el Viñedo (Ajusta estos valores con tus medidas reales)
        inicio_vinedo = 12.0  # A cuántos metros de la cortina empieza el viñedo
        fin_vinedo = 60.0     # A cuántos metros termina
        altura_vinedo = 1.2   # Altura de las vides
        
        # Dibujamos un rectángulo verde semitransparente para representar el cultivo
        figura.add_shape(
            type="rect",
            x0=inicio_vinedo, x1=fin_vinedo, y0=0, y1=altura_vinedo,
            fillcolor="rgba(34, 139, 34, 0.2)", # Verde suave
            line_width=1,
            line_color="rgba(34, 139, 34, 0.5)",
            layer="below"
        )
        
        # Trazo invisible solo para que el "Viñedo" aparezca en la leyenda
        figura.add_trace(go.Scatter(
            x=[inicio_vinedo, fin_vinedo], y=[0, 0], 
            mode="lines",
            line=dict(color="rgba(34, 139, 34, 0.5)", width=4),
            name="Zona de Viñedo"
        ))
        
        # Ajustes finales de formato
        figura.update_yaxes(rangemode="tozero")
        figura.update_layout(
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, bgcolor="rgba(255,255,255,0.8)")
        )
        
        st.plotly_chart(figura, use_container_width=True)
    else:
        st.warning(f"No hay puntos con velocidad menor a {velocidad} m/s en esta simulación.")

# --- SECCIÓN DE LOGOS ---
col_logo1, col_espacio, col_logo2 = st.columns([1, 4, 1])

with col_logo1:
    st.image("logo UTNFRM.png", use_container_width=True)

with col_logo2:
    st.image("Logo Iemi.png", use_container_width=True)
# ------------------------------

st.title("Simulaciones CFD con OpenFOAM")
st.write("Visualización interactiva de resultados de investigación en dinámica de fluidos.")

# Creamos la casilla de verificación
modo_comparacion = st.checkbox("Activar modo de comparación simultánea")
st.divider() 

# --- LÓGICA PRINCIPAL (VIDEOS Y GRÁFICAS) ---
if modo_comparacion:
    # MODO COMPARACIÓN
    st.header("Comparación de Modelos de Turbulencia")
    st.info("Comparativa directa: Modelo k-epsilon (izq.) vs Modelo k-omega (der.)")
     
    st.video("Comparación modelo k-ep_k-om.mp4") 
    
    # Gráficas interactivas en dos columnas (Asumimos que la comparativa es a velocidad alta 18m/s)
    st.divider()
    st.subheader("Análisis Interactivo de la Estela Protectora ")
    velocidad_elegida = st.slider("Velocidad límite de protección (m/s):", min_value=1.0, max_value=8.0, value=3.8, step=0.1, key="slider_comp")
    
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        df_ep = cargar_datos("datos_estela_maestro_e18.csv")
        graficar_estela(df_ep, velocidad_elegida, "Estela - Modelo k-epsilon")
        
    with col_graf2:
        df_om = cargar_datos("datos_estela_maestro_o18.csv")
        graficar_estela(df_om, velocidad_elegida, "Estela - Modelo k-omega")

else:
    # MODO INDIVIDUAL
    st.header("Visualización Individual")
        
    # Diccionario con las opciones: Vinculamos el video MP4 con su respectivo CSV
    modelos_datos = {
        "Modelo k-epsilon - Velocidad Baja": ("epsilon 10_2.mp4", "datos_estela_maestro_e10.csv"),
        "Modelo k-epsilon - Velocidad Alta": ("epsilon 18_2.mp4", "datos_estela_maestro_e18.csv"),
        "Modelo k-omega - Velocidad Baja": ("omega 10_2.mp4", "datos_estela_maestro_o10.csv"),
        "Modelo k-omega - Velocidad Alta": ("omega18_2.mp4", "datos_estela_maestro_o18.csv")
    }
    
    opcion_seleccionada = st.selectbox(
        "Selecciona el modelo y condición a visualizar:",
        list(modelos_datos.keys())
    )
    
    # Desempaquetamos los archivos correspondientes a la opción
    archivo_video, archivo_csv = modelos_datos[opcion_seleccionada]
    
    st.video(archivo_video)
    
    # Gráfica interactiva individual
    st.divider()
    st.subheader("Análisis Interactivo de la Estela Protectora 📊")
    velocidad_elegida = st.slider("Velocidad límite de protección (m/s):", min_value=1.0, max_value=8.0, value=3.8, step=0.1, key="slider_ind")
    
    df_ind = cargar_datos(archivo_csv)
    graficar_estela(df_ind, velocidad_elegida, f"Resultados para {opcion_seleccionada}")

st.divider()

# --- GEOMETRÍA 3D ---
st.header("Geometría del Dominio")
st.info("Interactúa con la maqueta 3D. Gira y haz zoom para explorar.")

ver_cotas = st.toggle("Mostrar cotas y medidas", value=True)
visibilidad_cotas = "block" if ver_cotas else "none"

with open("buildings.glb", "rb") as f:
    datos_3d = f.read()
    b64_3d = base64.b64encode(datos_3d).decode("utf-8")

codigo_html = f'''
<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
<style>
  .Hotspot {{
    border: none;
    background: none;
  }}
  .HotspotAnnotation {{
    display: {visibilidad_cotas};
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
    
    <button class="Hotspot" slot="hotspot-2" data-position="-8.284491645009238m 2.856832355316076m 6.9725749521763305m" data-normal="0.20547094633143412m -0.3993009764151941m 0.8934989761871793m">
        <div class="HotspotAnnotation">Altura 6.6 m</div>
    </button>
    
    <button class="Hotspot" slot="hotspot-4" data-position="5.9664710343985945m 2.9266600608825684m 1.171391566237828m" data-normal="0m -1m 0m">
        <div class="HotspotAnnotation">Altura 1.2 m</div>
    </button>
    
    <button class="Hotspot" slot="hotspot-7" data-position="-9.5119758273059m 0.2637165148610574m 6.196090438763218m" data-normal="-0.384493833891953m -0.14521766241229278m 0.911633875096015m">
        <div class="HotspotAnnotation">Altura 6 m</div>
    </button>
</model-viewer>
'''

components.html(codigo_html, height=550)