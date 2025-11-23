import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Clarito ☕",
    page_icon="☕",
    layout="centered"
)

# Estilos para que parezca App de celular
st.markdown("""
    <style>
    .stApp {background-color: #FAFAFA;}
    h1 {color: #4F3A2A; font-size: 28px !important;}
    div.stButton > button {
        background-color: #D2691E; 
        color: white; 
        border-radius: 12px; 
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN CON LA IA (SECRETS) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Falta la API Key. Configúrala en los 'Secrets' de Streamlit.")
    st.stop()

# --- 3. INTERFAZ DE USUARIO ---
st.title("☕ Clarito: Tu Sommelier")
st.write("Subí la foto de tu paquete. Te explico qué es, cómo hacerlo y con qué comerlo.")

# Pregunta clave para la receta
metodo_usuario = st.selectbox(
    "¿Qué cafetera vas a usar?",
    ("No sé, recomendame vos", "Prensa Francesa", "Cafetera Moka (Italiana)", "Filtro (V60/Melitta)", "Espresso", "Cafetera Eléctrica Común")
)

# Botón para subir foto o usar cámara
archivo = st.file_uploader("📸 Saca una foto a la etiqueta", type=["jpg", "png", "jpeg"])

# --- 4. EL CEREBRO DE LA IA (VERSIÓN PRO BARISTA & GOURMET) ---
def analizar_cafe(imagen, metodo):
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    prompt = f"""
    Actúa como un Juez del Campeonato Mundial de Baristas y Crítico Gastronómico Uruguayo.
    Analiza la imagen de esta etiqueta de café.
    
    El usuario seleccionó la cafetera: {metodo}.

    --- 🧠 LÓGICA DE EXTRACCIÓN (SCA STANDARDS) ---
    Para recomendar la receta, analiza visualmente el TUESTE y lee el PROCESO (Lavado, Natural, Honey):
    1. Si es Tueste Claro/Medio + Lavado -> Sugiere resaltar acidez y claridad (Ratios 1:16, temperaturas 92-94°C).
    2. Si es Tueste Medio/Oscuro + Natural -> Sugiere resaltar cuerpo y dulzura (Ratios 1:15, temperaturas 88-90°C).
    3. Si el usuario eligió "Recomendame vos":
       - Para cafés complejos/florales -> Recomienda Filtro (V60/Kalita).
       - Para cafés con notas a chocolate/frutos secos -> Recomienda Prensa Francesa o Cafetera Italiana.
    
    --- 🥐 BASE DE DATOS DE MARIDAJE URUGUAYO (VARIEDAD) ---
    NO RECOMIENDES SIEMPRE LO MISMO. Selecciona algo distinto basado en la "Nota Dominante" del café:
    
    [Opción Salada - Mañana/Tarde]
    - Tostado Mixto (Jamón y Queso) en pan de miga.
    - Sándwich Caliente (con muzzarella).
    - Tarta Pascualina (si es un café muy herbal).
    - Pan de Campo con aceite de oliva (para cafés muy ácidos).
    - Scones de Queso (Clásico).

    [Opción Dulce - Panadería]
    - Ojitos (masa seca con dulce de membrillo).
    - Margaritas (con crema pastelera).
    - Polvorones.
    - Coquitos.
    - Bizcochos de Grasa (Cuernitos/Vigilantes) -> Ideales para cafés con cuerpo.
    - Salchichón de Chocolate (Solo para cafés muy intensos/amargos).
    - Torta de Ricota.
    - Pasta Frola (Dulce de Leche o Membrillo según la acidez del café).
    - Carrot Cake o Budín de Limón (Cafetería moderna).

    --- ESTRUCTURA DE RESPUESTA ---
    Usa un tono Profesional pero Rioplatense.

    ### 🧐 Ficha Técnica
    (Resume Variedad, Proceso y Altura. Describe el perfil sensorial sin usar palabras raras).

    ### 🧪 La Receta del Experto ({metodo})
    (Basa tu recomendación en estándares internacionales. Da Ratio exacto (gr de café por ml de agua), Temperatura precisa y Molienda. Explica POR QUÉ esa receta mejora este grano específico).

    ### 🍽️ Maridaje Recomendado
    (Elige UNA opción Salada O Dulce de la lista de arriba que genere una "explosión de sabor" con este café. No seas aburrido. Explica el porqué de la combinación).
    """
    
    try:
        with st.spinner('Consultando estándares SCA y vitrinas de panadería... 🥐'):
            response = model.generate_content([prompt, imagen])
            return response.text
    except Exception as e:
        return f"Ups, error técnico leyendo la etiqueta: {e}"
    
    try:
        with st.spinner('Analizando etiqueta y buscando un bizcocho... 🧉'):
            response = model.generate_content([prompt, imagen])
            return response.text
    except Exception as e:
        return f"Ups, no pude leer bien. Probá sacar la foto más de cerca. Error técnico: {e}"

# --- 5. MOSTRAR RESULTADO ---
if archivo is not None:
    image = Image.open(archivo)
    st.image(image, use_column_width=True, caption="Tu Café")
    
    if st.button('✨ Analizar Ahora'):
        resultado = analizar_cafe(image, metodo_usuario)
        st.markdown(resultado)
        st.success("¡Que lo disfrutes!")
